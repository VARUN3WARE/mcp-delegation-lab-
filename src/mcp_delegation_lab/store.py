from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional


@dataclass
class Account:
    account_id: str
    owner: str
    balances: Dict[str, int]


@dataclass
class Delegation:
    delegation_id: str
    delegatee: str
    from_account: str
    allowed_tokens: List[str]
    max_amount: int
    expires_at: datetime
    policy_tags: List[str]


class MockUnitsStore:
    def __init__(self) -> None:
        self._accounts: Dict[str, Account] = {}
        self._delegations: Dict[str, Delegation] = {}

    @classmethod
    def seed_default(cls) -> "MockUnitsStore":
        store = cls()
        store._accounts = {
            "acct_001": Account(
                account_id="acct_001",
                owner="user_001",
                balances={"INR_STABLE": 5000},
            ),
            "acct_002": Account(
                account_id="acct_002",
                owner="user_002",
                balances={"INR_STABLE": 0},
            ),
        }
        store._delegations = {
            "del_001": Delegation(
                delegation_id="del_001",
                delegatee="agent_abc",
                from_account="acct_001",
                allowed_tokens=["INR_STABLE"],
                max_amount=1000,
                expires_at=datetime.now(timezone.utc) + timedelta(days=7),
                policy_tags=["demo"],
            ),
        }
        return store

    def get_account(self, account_id: str) -> Optional[Account]:
        return self._accounts.get(account_id)

    def get_delegation(self, delegation_id: str) -> Optional[Delegation]:
        return self._delegations.get(delegation_id)

    def apply_transfer(self, from_account: str, to_account: str, token_class: str, amount: int) -> None:
        source = self._accounts[from_account]
        target = self._accounts[to_account]
        source.balances[token_class] = source.balances.get(token_class, 0) - amount
        target.balances[token_class] = target.balances.get(token_class, 0) + amount
