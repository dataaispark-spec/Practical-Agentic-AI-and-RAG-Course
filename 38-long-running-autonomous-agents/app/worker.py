"""Deterministic reference implementation for Module 38.

The implementation intentionally models the control-plane mechanics that a
production durable worker needs: versioned task state, lease fencing,
checkpointing, idempotent effect records, approval binding, cumulative
budgets, cancellation and reconciliation after uncertain external effects.
It is an educational in-memory model, not a distributed queue/database.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Set, Tuple


class Status(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DEAD_LETTER = "dead_letter"


class Decision(str, Enum):
    CONTINUE = "continue"
    WAIT = "wait"
    COMPLETE = "complete"
    RETRY = "retry"
    ESCALATE = "escalate"
    CANCEL = "cancel"


@dataclass(frozen=True)
class Lease:
    worker_id: str
    fence: int
    expires_at: int


@dataclass
class Budget:
    max_steps: int = 100
    max_tool_calls: int = 100
    max_cost: float = 10.0
    steps: int = 0
    tool_calls: int = 0
    cost: float = 0.0

    def can_spend(self, *, steps: int = 0, tool_calls: int = 0, cost: float = 0.0) -> bool:
        return (
            self.steps + steps <= self.max_steps
            and self.tool_calls + tool_calls <= self.max_tool_calls
            and self.cost + cost <= self.max_cost + 1e-12
        )

    def spend(self, *, steps: int = 0, tool_calls: int = 0, cost: float = 0.0) -> None:
        if not self.can_spend(steps=steps, tool_calls=tool_calls, cost=cost):
            raise RuntimeError("cumulative budget exhausted")
        self.steps += steps
        self.tool_calls += tool_calls
        self.cost += cost


@dataclass
class EffectRecord:
    effect_id: str
    status: str = "pending"  # pending, applied, unknown, reconciled
    result: Optional[str] = None
    attempts: int = 0


@dataclass
class DurableJob:
    job_id: str
    goal: str
    total_steps: int = 5
    tenant: str = "default"
    status: Status = Status.CREATED
    checkpoint: int = 0
    state_version: int = 0
    attempts: int = 0
    history: List[str] = field(default_factory=list)
    effects: Dict[str, EffectRecord] = field(default_factory=dict)
    budget: Budget = field(default_factory=Budget)
    lease: Optional[Lease] = None
    cancelled: bool = False
    wait_reason: Optional[str] = None
    approval_hash: Optional[str] = None
    policy_version: str = "v1"

    @property
    def completed_effect_ids(self) -> Set[str]:
        return {k for k, v in self.effects.items() if v.status in {"applied", "reconciled"}}


class DurableStore:
    """Small authoritative store used to demonstrate optimistic concurrency."""

    def __init__(self) -> None:
        self.jobs: Dict[str, DurableJob] = {}
        self._next_fence = 0

    def put(self, job: DurableJob) -> None:
        self.jobs[job.job_id] = job

    def get(self, job_id: str) -> DurableJob:
        return self.jobs[job_id]

    def acquire_lease(self, job_id: str, worker_id: str, now: int, ttl: int = 10) -> Lease:
        job = self.get(job_id)
        if job.lease and job.lease.expires_at > now and job.lease.worker_id != worker_id:
            raise RuntimeError("lease is held by another worker")
        self._next_fence += 1
        job.lease = Lease(worker_id, self._next_fence, now + ttl)
        return job.lease

    def renew_lease(self, job_id: str, worker_id: str, fence: int, now: int, ttl: int = 10) -> None:
        job = self.get(job_id)
        self._assert_fence(job, worker_id, fence, now)
        job.lease = Lease(worker_id, fence, now + ttl)

    @staticmethod
    def _assert_fence(job: DurableJob, worker_id: str, fence: int, now: int) -> None:
        if not job.lease or job.lease.worker_id != worker_id or job.lease.fence != fence:
            raise RuntimeError("stale worker rejected by fencing token")
        if job.lease.expires_at <= now:
            raise RuntimeError("expired lease")

    def commit_checkpoint(self, job_id: str, worker_id: str, fence: int, now: int, checkpoint: int) -> None:
        job = self.get(job_id)
        self._assert_fence(job, worker_id, fence, now)
        if checkpoint < job.checkpoint:
            raise RuntimeError("checkpoint regression")
        job.checkpoint = checkpoint
        job.state_version += 1


class DurableWorker:
    """A deterministic worker with explicit effect and recovery semantics."""

    def __init__(self, effect: Callable[[str], str], store: Optional[DurableStore] = None) -> None:
        self.effect = effect
        self.store = store or DurableStore()

    def run(
        self,
        job: DurableJob,
        *,
        worker_id: str = "worker-1",
        now: int = 0,
        steps: Optional[int] = None,
        cost_per_step: float = 0.1,
        crash_after_effect_at: Optional[int] = None,
    ) -> DurableJob:
        if job.job_id not in self.store.jobs:
            self.store.put(job)
        job = self.store.get(job.job_id)
        if job.cancelled or job.status is Status.CANCELLED:
            job.status = Status.CANCELLED
            return job
        if job.status is Status.WAITING:
            return job
        lease = self.store.acquire_lease(job.job_id, worker_id, now)
        job.status = Status.RUNNING
        job.attempts += 1
        target = min(job.total_steps, steps if steps is not None else job.total_steps)

        for index in range(job.checkpoint, target):
            if not job.budget.can_spend(steps=1, tool_calls=1, cost=cost_per_step):
                job.status = Status.FAILED
                job.history.append("budget_exhausted")
                return job
            effect_id = f"{job.job_id}:effect:{index}"
            record = job.effects.setdefault(effect_id, EffectRecord(effect_id))
            if record.status in {"applied", "reconciled"}:
                self.store.commit_checkpoint(job.job_id, worker_id, lease.fence, now, index + 1)
                continue
            record.attempts += 1
            # The external call is deliberately separated from the ledger update:
            # a timeout can leave the effect status unknown.
            result = self.effect(effect_id)
            record.status = "applied"
            record.result = result
            job.budget.spend(steps=1, tool_calls=1, cost=cost_per_step)
            job.history.append(result)
            if crash_after_effect_at == index:
                job.status = Status.FAILED
                # checkpoint intentionally remains behind the effect; recovery
                # must use the effect ledger rather than execute it twice.
                return job
            self.store.commit_checkpoint(job.job_id, worker_id, lease.fence, now, index + 1)
        job.status = Status.COMPLETED if job.checkpoint >= job.total_steps else Status.RUNNING
        return job

    def wait(self, job: DurableJob, reason: str) -> DurableJob:
        job.status = Status.WAITING
        job.wait_reason = reason
        return job

    def resume(self, job: DurableJob) -> DurableJob:
        if job.status is not Status.WAITING:
            raise ValueError("job is not waiting")
        job.status = Status.CREATED
        job.wait_reason = None
        return job

    def cancel(self, job: DurableJob) -> DurableJob:
        job.cancelled = True
        job.status = Status.CANCELLED
        return job

    def reconcile(self, job: DurableJob, effect_id: str, external_result: str) -> DurableJob:
        record = job.effects.setdefault(effect_id, EffectRecord(effect_id))
        if record.status == "applied":
            return job
        record.status = "reconciled"
        record.result = external_result
        return job

    def bind_approval(self, job: DurableJob, action_hash: str, policy_version: str) -> None:
        job.approval_hash = action_hash
        job.policy_version = policy_version

    def authorize(self, job: DurableJob, action_hash: str, current_policy_version: str) -> bool:
        return bool(job.approval_hash == action_hash and job.policy_version == current_policy_version)


def retry_amplification(initial: int, retries: int, fanout: int) -> int:
    """Worst-case attempted calls when every retry fans out to ``fanout`` work."""
    total = 0
    batch = initial
    for _ in range(retries + 1):
        total += batch
        batch *= fanout
    return total
