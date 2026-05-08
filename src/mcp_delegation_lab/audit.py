from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4


class AuditLogger:
    def __init__(self) -> None:
        self._events: List[Dict[str, Any]] = []

    def log(self, event_type: str, payload: Dict[str, Any]) -> str:
        event_id = str(uuid4())
        event = {
            "id": event_id,
            "ts": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "payload": payload,
        }
        self._events.append(event)
        return event_id

    def list_events(self) -> List[Dict[str, Any]]:
        return list(self._events)
