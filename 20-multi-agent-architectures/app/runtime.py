from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import time
import uuid


class ContractError(Exception):
    pass


@dataclass(frozen=True)
class TaskEnvelope:
    task_id: str
    parent_id: str | None
    tenant_id: str
    worker: str
    capabilities: frozenset[str]
    payload: dict[str, object]
    deadline: float
    idempotency_key: str


@dataclass(frozen=True)
class WorkerResult:
    task_id: str
    worker: str
    ok: bool
    evidence: list[str]
    confidence: float
    error: str | None = None


class Worker:
    name = "base"
    capabilities: frozenset[str] = frozenset()

    def run(self, task: TaskEnvelope) -> WorkerResult:
        raise NotImplementedError


class WorkerRegistry:
    def __init__(self, workers: list[Worker]):
        self.workers = {w.name: w for w in workers}

    def get(self, name: str, capabilities: frozenset[str]) -> Worker:
        worker = self.workers.get(name)
        if not worker:
            raise ContractError(f"unknown worker: {name}")
        if not capabilities.issubset(worker.capabilities):
            raise ContractError("requested worker capabilities exceed worker contract")
        return worker


class SupervisorRuntime:
    def __init__(self, registry: WorkerRegistry, *, max_workers: int = 4, max_depth: int = 3):
        self.registry = registry
        self.max_workers = max_workers
        self.max_depth = max_depth
        self.completed: set[str] = set()

    def envelope(self, *, tenant_id: str, worker: str, capabilities: frozenset[str], payload: dict,
                 parent_id: str | None = None, timeout_s: float = 10.0) -> TaskEnvelope:
        if parent_id and parent_id.count("/") >= self.max_depth:
            raise ContractError("delegation depth exceeded")
        task_id = str(uuid.uuid4())
        return TaskEnvelope(task_id, parent_id, tenant_id, worker, capabilities, payload,
                            time.monotonic() + timeout_s, str(uuid.uuid4()))

    def dispatch(self, task: TaskEnvelope) -> WorkerResult:
        if task.task_id in self.completed:
            return WorkerResult(task.task_id, task.worker, True, ["deduplicated"], 1.0)
        if time.monotonic() >= task.deadline:
            return WorkerResult(task.task_id, task.worker, False, [], 0.0, "deadline exceeded")
        worker = self.registry.get(task.worker, task.capabilities)
        result = worker.run(task)
        if result.ok:
            self.completed.add(task.task_id)
        return result

    def fan_out(self, tasks: list[TaskEnvelope]) -> list[WorkerResult]:
        results: list[WorkerResult] = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {pool.submit(self.dispatch, t): t for t in tasks}
            for future in as_completed(futures):
                results.append(future.result())
        return results

    @staticmethod
    def validate_result(result: WorkerResult) -> None:
        if not result.task_id or not result.worker:
            raise ContractError("missing result identity")
        if not 0 <= result.confidence <= 1:
            raise ContractError("confidence must be between 0 and 1")
        if result.ok and not result.evidence:
            raise ContractError("successful result requires evidence")
