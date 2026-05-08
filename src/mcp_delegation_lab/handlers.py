from __future__ import annotations

from typing import Any, Dict
from uuid import uuid4

from pydantic import ValidationError

from .audit import AuditLogger
from .errors import ErrorCode, ToolError, error_result, ok_result
from .models import DelegationScopeOut, TransferReceipt, TransferRequest
from .policy import PolicyEngine
from .store import MockUnitsStore


def get_delegation_scope(store: MockUnitsStore, audit: AuditLogger, delegation_id: str) -> Dict[str, Any]:
    delegation = store.get_delegation(delegation_id)
    audit_id = audit.log("get_delegation_scope", {"delegation_id": delegation_id})
    if delegation is None:
        return error_result(
            ToolError(
                code=ErrorCode.NOT_FOUND,
                message="Delegation not found.",
                detail={"delegation_id": delegation_id},
            ),
            audit_id=audit_id,
        )

    scope = DelegationScopeOut(
        delegation_id=delegation.delegation_id,
        delegatee=delegation.delegatee,
        allowed_tokens=delegation.allowed_tokens,
        max_amount=str(delegation.max_amount),
        expires_at=delegation.expires_at.isoformat(),
        policy_tags=delegation.policy_tags,
    )
    return ok_result(scope.model_dump(), audit_id=audit_id)


def check_transfer_eligibility(
    store: MockUnitsStore,
    audit: AuditLogger,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    audit_id = audit.log("check_transfer_eligibility", payload)
    try:
        request = TransferRequest.model_validate(payload)
    except ValidationError as exc:
        return error_result(
            ToolError(
                code=ErrorCode.VALIDATION_ERROR,
                message="Invalid request payload.",
                detail={"errors": exc.errors()},
            ),
            audit_id=audit_id,
        )

    delegation = store.get_delegation(request.delegation_id)
    if delegation is None:
        return error_result(
            ToolError(
                code=ErrorCode.NOT_FOUND,
                message="Delegation not found.",
                detail={"delegation_id": request.delegation_id},
            ),
            audit_id=audit_id,
        )

    from_account = store.get_account(request.from_account)
    if from_account is None:
        return error_result(
            ToolError(
                code=ErrorCode.NOT_FOUND,
                message="Source account not found.",
                detail={"from_account": request.from_account},
            ),
            audit_id=audit_id,
        )

    to_account = store.get_account(request.to_account)
    if to_account is None:
        return error_result(
            ToolError(
                code=ErrorCode.NOT_FOUND,
                message="Destination account not found.",
                detail={"to_account": request.to_account},
            ),
            audit_id=audit_id,
        )

    policy = PolicyEngine()
    eligibility = policy.evaluate(request, delegation, from_account)
    return ok_result(eligibility.model_dump(), audit_id=audit_id)


def initiate_transfer(
    store: MockUnitsStore,
    audit: AuditLogger,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    audit_id = audit.log("initiate_transfer", payload)
    try:
        request = TransferRequest.model_validate(payload)
    except ValidationError as exc:
        return error_result(
            ToolError(
                code=ErrorCode.VALIDATION_ERROR,
                message="Invalid request payload.",
                detail={"errors": exc.errors()},
            ),
            audit_id=audit_id,
        )

    delegation = store.get_delegation(request.delegation_id)
    if delegation is None:
        return error_result(
            ToolError(
                code=ErrorCode.NOT_FOUND,
                message="Delegation not found.",
                detail={"delegation_id": request.delegation_id},
            ),
            audit_id=audit_id,
        )

    from_account = store.get_account(request.from_account)
    to_account = store.get_account(request.to_account)
    if from_account is None or to_account is None:
        return error_result(
            ToolError(
                code=ErrorCode.NOT_FOUND,
                message="Account not found.",
                detail={
                    "from_account": request.from_account,
                    "to_account": request.to_account,
                },
            ),
            audit_id=audit_id,
        )

    policy = PolicyEngine()
    eligibility = policy.evaluate(request, delegation, from_account)
    if not eligibility.eligible:
        return error_result(
            ToolError(
                code=ErrorCode(eligibility.code),
                message=eligibility.message or "Policy checks failed.",
                detail=eligibility.detail.model_dump(),
            ),
            audit_id=audit_id,
        )

    amount_value = int(request.amount)
    store.apply_transfer(
        request.from_account,
        request.to_account,
        request.token_class,
        amount_value,
    )

    receipt = TransferReceipt(
        transfer_id=f"tr_{uuid4().hex}",
        status="committed",
        executed_at=audit.list_events()[-1]["ts"],
        from_account=request.from_account,
        to_account=request.to_account,
        token_class=request.token_class,
        amount=request.amount,
        audit_id=audit_id,
        policy_result=eligibility,
    )
    return ok_result(receipt.model_dump(), audit_id=audit_id)
