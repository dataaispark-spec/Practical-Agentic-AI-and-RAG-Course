from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Any, Callable


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    input: str
    expected: Any
    required_evidence: tuple[str, ...] = ()
    forbidden: tuple[str, ...] = ()
    risk: str = "normal"
    max_cost_usd: float | None = None
    max_latency_ms: float | None = None


@dataclass(frozen=True)
class EvalResult:
    case_id: str
    success: bool
    quality: float
    safety: bool
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Gate:
    min_success: float = 0.0
    min_quality: float = 0.0
    max_cost_per_success: float | None = None
    max_latency_ms: float | None = None
    require_safety: bool = True


def score_case(case: EvalCase, output: Any, *, evidence: list[str] | None = None, cost_usd: float = 0.0, latency_ms: float = 0.0) -> EvalResult:
    text = str(output)
    success = str(case.expected).lower() in text.lower()
    forbidden_hit = any(x.lower() in text.lower() for x in case.forbidden)
    evidence = evidence or []
    evidence_coverage = (sum(x in evidence for x in case.required_evidence) / len(case.required_evidence)) if case.required_evidence else 1.0
    quality = (1.0 if success else 0.0) * 0.6 + evidence_coverage * 0.4
    safety = not forbidden_hit
    return EvalResult(case.case_id, success, quality, safety, cost_usd, latency_ms, {"evidence_coverage": evidence_coverage, "forbidden_hit": forbidden_hit})


def summarize(results: list[EvalResult]) -> dict[str, float]:
    if not results:
        return {"success_rate": 0.0, "mean_quality": 0.0, "safety_rate": 0.0, "cost_per_success": 0.0, "mean_latency_ms": 0.0}
    successes = sum(r.success for r in results)
    return {
        "success_rate": successes / len(results),
        "mean_quality": sum(r.quality for r in results) / len(results),
        "safety_rate": sum(r.safety for r in results) / len(results),
        "cost_per_success": sum(r.cost_usd for r in results) / successes if successes else float("inf"),
        "mean_latency_ms": sum(r.latency_ms for r in results) / len(results),
    }


def gate(results: list[EvalResult], policy: Gate) -> tuple[bool, list[str]]:
    m = summarize(results)
    failures: list[str] = []
    if m["success_rate"] < policy.min_success: failures.append("success_rate")
    if m["mean_quality"] < policy.min_quality: failures.append("quality")
    if policy.require_safety and m["safety_rate"] < 1.0: failures.append("safety")
    if policy.max_cost_per_success is not None and m["cost_per_success"] > policy.max_cost_per_success: failures.append("cost")
    if policy.max_latency_ms is not None and m["mean_latency_ms"] > policy.max_latency_ms: failures.append("latency")
    return not failures, failures


def bootstrap_delta(a: list[float], b: list[float]) -> tuple[float, float]:
    """Simple paired mean delta and normal-approx 95% interval."""
    if len(a) != len(b) or not a:
        raise ValueError("paired samples must have equal non-zero length")
    deltas = [x - y for x, y in zip(a, b)]
    mean = sum(deltas) / len(deltas)
    if len(deltas) == 1:
        return mean, mean
    variance = sum((x - mean) ** 2 for x in deltas) / (len(deltas) - 1)
    margin = 1.96 * sqrt(variance / len(deltas))
    return mean, (mean - margin, mean + margin)


def slice_results(results: list[EvalResult], key: str) -> dict[Any, list[EvalResult]]:
    output: dict[Any, list[EvalResult]] = {}
    for r in results:
        value = r.details.get(key, "unknown")
        output.setdefault(value, []).append(r)
    return output
