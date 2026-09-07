from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
import time
import uuid


class TaskStatus(str, Enum):
    PENDING = "pending"
    LEASED = "leased"
    COMPLETED = "completed"
    RECOVERABLE = "recoverable"
    CANCELLED = "cancelled"
    DEAD_LETTER = "dead_letter"


class FailureClass(str, Enum):
    TRANSIENT = "transient"
    PERMANENT = "permanent"
    AUTHORIZATION = "authorization"
    TIMEOUT = "timeout"


@dataclass(frozen=True)
class Message:
    message_id: str
    correlation_id: str
    causation_id: str | None
    sender: str
    receiver: str
    tenant_id: str
    schema_version: str
    payload: dict[str, object]
    idempotency_key: str
    expires_at: float


@dataclass
class Task:
    task_id: str
    tenant_id: str
    status: TaskStatus = TaskStatus.PENDING
    lease_id: str | None = None
    lease_until: float | None = None
    attempts: int = 0
    result: object | None = None
    cancellation_requested: bool = False
    history: list[str] = field(default_factory=list)


class CoordinationError(Exception):
    pass


class TaskCoordinator:
    def __init__(self, *, lease_seconds: float = 30.0, max_attempts: int = 3):
        self.lease_seconds = lease_seconds
        self.max_attempts = max_attempts
        self.tasks: dict[str, Task] = {}
        self.effects: dict[str, object] = {}

    def create(self, tenant_id: str) -> Task:
        task = Task(str(uuid.uuid4()), tenant_id)
        self.tasks[task.task_id] = task
        return task

    def claim(self, task_id: str, worker_id: str) -> str:
        task = self.tasks[task_id]
        now = time.monotonic()
        if task.status == TaskStatus.CANCELLED:
            raise CoordinationError("task cancelled")
        if task.status == TaskStatus.LEASED and task.lease_until and task.lease_until > now:
            raise CoordinationError("task already leased")
        task.status = TaskStatus.LEASED
        task.lease_id = f"{worker_id}:{uuid.uuid4()}"
        task.lease_until = now + self.lease_seconds
        task.attempts += 1
        task.history.append(f"claimed:{task.lease_id}")
        return task.lease_id

    def heartbeat(self, task_id: str, lease_id: str) -> None:
        task = self.tasks[task_id]
        if task.status != TaskStatus.LEASED or task.lease_id != lease_id:
            raise CoordinationError("stale lease heartbeat")
        task.lease_until = time.monotonic() + self.lease_seconds

    def complete(self, task_id: str, lease_id: str, result: object) -> None:
        task = self.tasks[task_id]
        if task.status != TaskStatus.LEASED or task.lease_id != lease_id:
            raise CoordinationError("stale worker cannot commit")
        task.result = result
        task.status = TaskStatus.COMPLETED
        task.history.append("completed")

    def expire_leases(self) -> list[str]:
        now = time.monotonic()
        recovered = []
        for task in self.tasks.values():
            if task.status == TaskStatus.LEASED and task.lease_until and task.lease_until <= now:
                task.status = TaskStatus.RECOVERABLE
                task.history.append("lease_expired")
                recovered.append(task.task_id)
        return recovered

    def cancel(self, task_id: str) -> None:
        task = self.tasks[task_id]
        task.cancellation_requested = True
        task.status = TaskStatus.CANCELLED
        task.history.append("cancelled")

    def record_effect(self, idempotency_key: str, result: object) -> bool:
        """Returns False when the side effect was already recorded."""
        if idempotency_key in self.effects:
            return False
        self.effects[idempotency_key] = result
        return True

    def retry_or_dead_letter(self, task_id: str, failure: FailureClass) -> TaskStatus:
        task = self.tasks[task_id]
        retryable = failure in {FailureClass.TRANSIENT, FailureClass.TIMEOUT}
        if retryable and task.attempts < self.max_attempts:
            task.status = TaskStatus.PENDING
            task.history.append(f"retry:{failure.value}")
            return task.status
        task.status = TaskStatus.DEAD_LETTER
        task.history.append(f"dead_letter:{failure.value}")
        return task.status


def backoff(attempt: int, base: float = 0.5, cap: float = 30.0, jitter: float = 0.2) -> float:
    raw = min(cap, base * (2 ** max(0, attempt - 1)))
    return raw * random.uniform(1 - jitter, 1 + jitter)


def expired(message: Message, now: float | None = None) -> bool:
    return (time.monotonic() if now is None else now) >= message.expires_at
