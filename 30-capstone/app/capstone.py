from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json


class Phase(str, Enum):
    GOVERN = "govern"
    RETRIEVE = "retrieve"
    PLAN = "plan"
    ACT = "act"
    VERIFY = "verify"
    COMPLETE = "complete"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class CapstoneTask:
    task_id: str
    tenant_id: str
    goal: str
    risk: int
    budget_usd: float
    allowed_tools: frozenset[str] = frozenset()


@dataclass
class RunState:
    task: CapstoneTask
    phase: Phase = Phase.GOVERN
    evidence: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    verified: bool = False
    spent_usd: float = 0.0

    def consume(self, amount: float) -> None:
        if self.spent_usd + amount > self.task.budget_usd:
            raise RuntimeError("task budget exceeded")
        self.spent_usd += amount


def stable_action_id(task: CapstoneTask, action: str) -> str:
    payload = json.dumps({"task": task.task_id, "tenant": task.tenant_id, "action": action}, sort_keys=True)
    return sha256(payload.encode()).hexdigest()


def verify_completion(state: RunState, *, required_evidence: int = 1) -> bool:
    state.verified = bool(state.evidence) and len(state.evidence) >= required_evidence
    return state.verified
