"""Deterministic contracts around probabilistic agent decisions."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ActionClass(str, Enum):
    READ = "read"
    WRITE = "write"
    EXTERNAL_COMMUNICATION = "external_communication"
    FINANCIAL = "financial"
    DESTRUCTIVE = "destructive"
    ADMINISTRATIVE = "administrative"


@dataclass(frozen=True)
class TaskContract:
    task_id: str
    goal: str
    owner: str
    tenant: str
    risk_level: RiskLevel = RiskLevel.LOW
    time_budget_s: float = 60.0
    token_budget: int = 10_000
    tool_budget: int = 20
    action_budget: int = 30
    allowed_systems: tuple[str, ...] = ()
    required_approvals: tuple[ActionClass, ...] = ()
    success_conditions: tuple[str, ...] = ()
    expiry_epoch_s: float | None = None


@dataclass(frozen=True)
class ActionRequest:
    action_id: str
    task_id: str
    tool: str
    action_class: ActionClass
    arguments: dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    expected_state: str | None = None
    idempotency_key: str | None = None


@dataclass(frozen=True)
class VerificationResult:
    passed: bool
    verifier: str
    evidence: dict[str, Any] = field(default_factory=dict)
    message: str = ""
