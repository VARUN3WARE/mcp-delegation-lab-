from mcp_delegation_lab.audit import AuditLogger
from mcp_delegation_lab.handlers import (
    check_transfer_eligibility,
    get_delegation_scope,
    initiate_transfer,
)
from mcp_delegation_lab.store import MockUnitsStore


def test_get_delegation_scope_ok() -> None:
    store = MockUnitsStore.seed_default()
    audit = AuditLogger()
    result = get_delegation_scope(store, audit, "del_001")

    assert result["ok"] is True
    assert result["data"]["delegation_id"] == "del_001"


def test_check_transfer_eligibility_scope_exceeded() -> None:
    store = MockUnitsStore.seed_default()
    audit = AuditLogger()
    payload = {
        "delegation_id": "del_001",
        "from_account": "acct_001",
        "to_account": "acct_002",
        "token_class": "INR_STABLE",
        "amount": "1500",
    }
    result = check_transfer_eligibility(store, audit, payload)

    assert result["ok"] is True
    assert result["data"]["eligible"] is False
    assert result["data"]["code"] == "SCOPE_EXCEEDED"


def test_initiate_transfer_ok_updates_balance() -> None:
    store = MockUnitsStore.seed_default()
    audit = AuditLogger()
    payload = {
        "delegation_id": "del_001",
        "from_account": "acct_001",
        "to_account": "acct_002",
        "token_class": "INR_STABLE",
        "amount": "500",
    }
    result = initiate_transfer(store, audit, payload)

    assert result["ok"] is True
    assert store.get_account("acct_001").balances["INR_STABLE"] == 4500
    assert store.get_account("acct_002").balances["INR_STABLE"] == 500
