from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class TransferRequest(BaseModel):
    delegation_id: str = Field(..., min_length=3)
    from_account: str = Field(..., min_length=3)
    to_account: str = Field(..., min_length=3)
    token_class: str = Field(..., min_length=2)
    amount: str = Field(..., min_length=1)
    client_reference: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_digits(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("amount must be a positive integer string")
        if int(value) <= 0:
            raise ValueError("amount must be greater than zero")
        return value


class DelegationScopeOut(BaseModel):
    delegation_id: str
    delegatee: str
    allowed_tokens: List[str]
    max_amount: str
    expires_at: str
    policy_tags: List[str]


class EligibilityDetail(BaseModel):
    token_class: str
    requested_amount: str
    delegated_limit: str
    checks_failed: List[str]
    checks_passed: List[str]


class EligibilityResult(BaseModel):
    eligible: bool
    code: Optional[str] = None
    message: Optional[str] = None
    detail: EligibilityDetail


class TransferReceipt(BaseModel):
    transfer_id: str
    status: str
    executed_at: str
    from_account: str
    to_account: str
    token_class: str
    amount: str
    audit_id: str
    policy_result: EligibilityResult
