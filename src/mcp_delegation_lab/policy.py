from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Tuple

from .errors import ErrorCode
from .models import EligibilityDetail, EligibilityResult, TransferRequest
from .store import Account, Delegation


class PolicyEngine:
    def evaluate(
        self,
        request: TransferRequest,
        delegation: Delegation,
        from_account: Account,
    ) -> EligibilityResult:
        checks_passed: List[str] = []
        checks_failed: List[str] = []

        now = datetime.now(timezone.utc)
        if delegation.expires_at > now:
            checks_passed.append("delegation_active")
        else:
            checks_failed.append("delegation_expired")

        if request.token_class in delegation.allowed_tokens:
            checks_passed.append("token_class")
        else:
            checks_failed.append("token_class")

        if request.from_account == delegation.from_account:
            checks_passed.append("from_account_scope")
        else:
            checks_failed.append("from_account_scope")

        amount_value = int(request.amount)
        if amount_value <= delegation.max_amount:
            checks_passed.append("amount_limit")
        else:
            checks_failed.append("amount_limit")

        available_balance = from_account.balances.get(request.token_class, 0)
        if available_balance >= amount_value:
            checks_passed.append("sufficient_balance")
        else:
            checks_failed.append("sufficient_balance")

        detail = EligibilityDetail(
            token_class=request.token_class,
            requested_amount=request.amount,
            delegated_limit=str(delegation.max_amount),
            checks_failed=checks_failed,
            checks_passed=checks_passed,
        )

        if checks_failed:
            scope_failures = {"token_class", "from_account_scope", "amount_limit"}
            if any(item in scope_failures for item in checks_failed):
                code = ErrorCode.SCOPE_EXCEEDED.value
                message = "Requested transfer exceeds delegation scope."
            else:
                code = ErrorCode.POLICY_CHECK_FAILED.value
                message = "Policy checks failed."
            return EligibilityResult(
                eligible=False,
                code=code,
                message=message,
                detail=detail,
            )

        return EligibilityResult(
            eligible=True,
            code=None,
            message=None,
            detail=detail,
        )
