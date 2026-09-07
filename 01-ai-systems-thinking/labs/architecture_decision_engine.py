"""Explainable architecture selection for Module 1.

This deliberately uses plain Python so learners understand the decision mechanism
before introducing frameworks.
"""

from dataclasses import dataclass
from typing import Literal

Risk = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class Requirements:
    needs_generation: bool
    needs_knowledge: bool
    needs_actions: bool
    roles: int = 1
    risk: Risk = "low"
    human_approval: bool = False


@dataclass(frozen=True)
class ArchitectureRecommendation:
    recommended_pattern: str
    alternatives_considered: tuple[str, ...]
    reasons: tuple[str, ...]
    complexity_warning: str


def recommend(req: Requirements) -> ArchitectureRecommendation:
    """Return the minimum sufficient architecture with traceable reasons."""
    alternatives = ("deterministic_software", "llm_application", "rag", "agent_or_workflow", "multi_agent")

    if not req.needs_generation:
        return ArchitectureRecommendation(
            "deterministic_software", alternatives,
            ("generation is not required",),
            "Do not introduce an LLM without a measurable requirement.",
        )

    if not req.needs_knowledge and not req.needs_actions:
        return ArchitectureRecommendation(
            "llm_application", alternatives,
            ("generation is required", "no external/current knowledge is required", "no actions are required"),
            "Keep the control flow deterministic around the model.",
        )

    if req.needs_actions:
        if req.human_approval or req.risk == "high":
            return ArchitectureRecommendation(
                "rag_with_workflow_and_approval" if req.needs_knowledge else "workflow_with_approval",
                alternatives,
                ("actions are required", "high-risk or approval-gated action boundary exists"),
                "Never use the model as the authorization layer.",
            )
        if req.roles > 3:
            return ArchitectureRecommendation(
                "evaluate_multi_agent", alternatives,
                ("actions are required", "multiple independent roles may be useful"),
                "Prove multi-agent value against a single-agent/workflow baseline.",
            )
        return ArchitectureRecommendation(
            "agent_or_workflow", alternatives,
            ("actions are required",),
            "Bound tool calls, steps, latency, cost, and failure recovery.",
        )

    return ArchitectureRecommendation(
        "rag", alternatives,
        ("current/private knowledge is required",),
        "Treat retrieval quality and authorization as separate concerns.",
    )


def explain(req: Requirements) -> dict[str, object]:
    result = recommend(req)
    return {
        "recommended_pattern": result.recommended_pattern,
        "alternatives_considered": list(result.alternatives_considered),
        "reasons": list(result.reasons),
        "complexity_warning": result.complexity_warning,
    }


if __name__ == "__main__":
    example = Requirements(True, True, True, roles=1, risk="high", human_approval=True)
    print(explain(example))
