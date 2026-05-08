from __future__ import annotations

from typing import Any, Dict, Optional

from .audit import AuditLogger
from . import handlers
from .store import MockUnitsStore


def register_tools(mcp: Any, store: MockUnitsStore, audit: AuditLogger) -> None:
    @mcp.tool()
    def get_delegation_scope(delegation_id: str) -> Dict[str, Any]:
        return handlers.get_delegation_scope(store, audit, delegation_id)

    @mcp.tool()
    def check_transfer_eligibility(
        delegation_id: str,
        from_account: str,
        to_account: str,
        token_class: str,
        amount: str,
        client_reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "delegation_id": delegation_id,
            "from_account": from_account,
            "to_account": to_account,
            "token_class": token_class,
            "amount": amount,
            "client_reference": client_reference,
        }
        return handlers.check_transfer_eligibility(store, audit, payload)

    @mcp.tool()
    def initiate_transfer(
        delegation_id: str,
        from_account: str,
        to_account: str,
        token_class: str,
        amount: str,
        client_reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "delegation_id": delegation_id,
            "from_account": from_account,
            "to_account": to_account,
            "token_class": token_class,
            "amount": amount,
            "client_reference": client_reference,
        }
        return handlers.initiate_transfer(store, audit, payload)
