from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    input: str
    expected: Any
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelOutput:
    value: Any
    latency_ms: float
    cost_usd: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    passed: bool
    score: float
    failure_category: str | None
    latency_ms: float
    cost_usd: float
    details: dict[str, Any] = field(default_factory=dict)
