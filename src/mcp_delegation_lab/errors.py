from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class ErrorCode(str, Enum):
    SCOPE_EXCEEDED = "SCOPE_EXCEEDED"
    POLICY_CHECK_FAILED = "POLICY_CHECK_FAILED"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"


@dataclass
class ToolError:
    code: ErrorCode
    message: str
    detail: Optional[Dict[str, Any]] = None

    def as_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "code": self.code.value,
            "message": self.message,
        }
        if self.detail is not None:
            payload["detail"] = self.detail
        return payload


def ok_result(data: Any, audit_id: Optional[str] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "ok": True,
        "data": data,
    }
    if audit_id is not None:
        payload["audit_id"] = audit_id
    return payload


def error_result(error: ToolError, audit_id: Optional[str] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "ok": False,
        "error": error.as_dict(),
    }
    if audit_id is not None:
        payload["audit_id"] = audit_id
    return payload
