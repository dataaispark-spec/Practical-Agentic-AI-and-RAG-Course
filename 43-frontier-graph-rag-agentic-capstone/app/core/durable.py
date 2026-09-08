"""Durable execution primitives for AegisAI.

The implementation deliberately uses the Python standard library so learners can
understand the mechanics before introducing a database or workflow framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
import json
import threading
from typing import Any
from uuid import uuid4


class RunStatus(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Checkpoint:
    run_id: str
    sequence: int
    status: str
    state: dict[str, Any]
    created_at: str = field(default_factory=utc_now)


@dataclass
class RunRecord:
    run_id: str
    task_id: str
    status: RunStatus = RunStatus.CREATED
    sequence: int = 0
    state: dict[str, Any] = field(default_factory=dict)
    consumed_steps: int = 0
    consumed_tokens: int = 0
    consumed_tool_calls: int = 0
    idempotency_keys: set[str] = field(default_factory=set)
    updated_at: str = field(default_factory=utc_now)


class DurableRunStore:
    """Small append-safe JSON store used for teaching durable state.

    Production deployments should replace this with a transactional datastore,
    but the interface should remain stable.
    """

    def __init__(self, root: str | Path = ".aegisai/runs") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    def _path(self, run_id: str) -> Path:
        return self.root / f"{run_id}.json"

    def create(self, task_id: str, state: dict[str, Any] | None = None) -> RunRecord:
        record = RunRecord(run_id=str(uuid4()), task_id=task_id, state=state or {})
        self.save(record)
        return record

    def save(self, record: RunRecord) -> None:
        with self._lock:
            record.updated_at = utc_now()
            payload = asdict(record)
            payload["status"] = record.status.value
            payload["idempotency_keys"] = sorted(record.idempotency_keys)
            tmp = self._path(record.run_id).with_suffix(".tmp")
            tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
            tmp.replace(self._path(record.run_id))

    def load(self, run_id: str) -> RunRecord:
        with self._lock:
            payload = json.loads(self._path(run_id).read_text(encoding="utf-8"))
            payload["status"] = RunStatus(payload["status"])
            payload["idempotency_keys"] = set(payload.get("idempotency_keys", []))
            return RunRecord(**payload)

    def checkpoint(self, record: RunRecord) -> Checkpoint:
        record.sequence += 1
        checkpoint = Checkpoint(
            run_id=record.run_id,
            sequence=record.sequence,
            status=record.status.value,
            state=dict(record.state),
        )
        self.save(record)
        path = self.root / f"{record.run_id}.checkpoint.{checkpoint.sequence}.json"
        path.write_text(json.dumps(asdict(checkpoint), indent=2, sort_keys=True), encoding="utf-8")
        return checkpoint

    def mark_idempotency_key(self, record: RunRecord, key: str) -> bool:
        """Return False when a key was already consumed."""
        if key in record.idempotency_keys:
            return False
        record.idempotency_keys.add(key)
        self.save(record)
        return True

    def cancel(self, record: RunRecord) -> RunRecord:
        record.status = RunStatus.CANCELLED
        self.save(record)
        return record

    def list_runs(self) -> list[RunRecord]:
        return [self.load(p.stem) for p in self.root.glob("*.json") if ".checkpoint." not in p.name]
