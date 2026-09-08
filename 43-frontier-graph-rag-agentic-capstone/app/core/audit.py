"""Structured audit events for reconstructing an agent run."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AuditEvent:
    run_id: str
    event_type: str
    sequence: int
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=now)


class AuditLog:
    def __init__(self, path: str | Path = ".aegisai/audit.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: AuditEvent) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event), sort_keys=True) + "\n")

    def record(self, run_id: str, sequence: int, event_type: str, **data: Any) -> AuditEvent:
        event = AuditEvent(run_id=run_id, sequence=sequence, event_type=event_type, data=data)
        self.append(event)
        return event

    def for_run(self, run_id: str) -> list[AuditEvent]:
        if not self.path.exists():
            return []
        events: list[AuditEvent] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            if item["run_id"] == run_id:
                events.append(AuditEvent(**item))
        return events
