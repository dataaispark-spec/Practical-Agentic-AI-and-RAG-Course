from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Architecture(str, Enum):
    WORKFLOW = "deterministic_workflow"
    SINGLE_AGENT = "single_agent"
    MULTI_AGENT = "multi_agent"


@dataclass(frozen=True)
class Requirements:
    parallelism: float = 0.0
    specialization: float = 0.0
    decomposition: float = 0.0
    contractability: float = 0.0
    verification: float = 0.0
    latency_sensitivity: float = 0.5
    cost_sensitivity: float = 0.5
    coordination_risk: float = 0.5
    security_sensitivity: float = 0.5
    generation_need: float = 0.5


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def score_architectures(r: Requirements) -> dict[Architecture, float]:
    """Heuristic decision aid; benchmark results must override this score."""
    multi_gain = (
        0.24 * r.parallelism
        + 0.24 * r.specialization
        + 0.18 * r.decomposition
        + 0.18 * r.contractability
        + 0.16 * r.verification
        - 0.20 * r.latency_sensitivity
        - 0.18 * r.cost_sensitivity
        - 0.22 * r.coordination_risk
        - 0.14 * r.security_sensitivity
    )
    single = (
        0.35 * r.generation_need
        + 0.20 * r.verification
        + 0.15 * (1 - r.coordination_risk)
        + 0.12 * (1 - r.latency_sensitivity)
        + 0.10 * (1 - r.cost_sensitivity)
        + 0.08 * (1 - r.security_sensitivity)
    )
    workflow = (
        0.30 * (1 - r.generation_need)
        + 0.20 * r.verification
        + 0.18 * (1 - r.coordination_risk)
        + 0.15 * r.security_sensitivity
        + 0.10 * r.latency_sensitivity
        + 0.07 * r.cost_sensitivity
    )
    return {
        Architecture.WORKFLOW: _clamp(workflow),
        Architecture.SINGLE_AGENT: _clamp(single),
        Architecture.MULTI_AGENT: _clamp(0.5 + multi_gain),
    }


def recommend(r: Requirements) -> Architecture:
    scores = score_architectures(r)
    return max(scores, key=scores.get)


def should_upgrade_to_multi_agent(
    *, baseline_success: float, multi_success: float,
    baseline_cost: float, multi_cost: float,
    baseline_latency: float, multi_latency: float,
    minimum_success_gain: float = 0.05,
    max_cost_multiplier: float = 2.0,
    max_latency_multiplier: float = 2.0,
) -> bool:
    """Evidence gate: quality improvement must justify cost/latency expansion."""
    if multi_success - baseline_success < minimum_success_gain:
        return False
    if baseline_cost > 0 and multi_cost / baseline_cost > max_cost_multiplier:
        return False
    if baseline_latency > 0 and multi_latency / baseline_latency > max_latency_multiplier:
        return False
    return True
