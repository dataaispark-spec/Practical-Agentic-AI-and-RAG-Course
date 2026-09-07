from models import Requirements, Risk


def recommend(req: Requirements) -> dict:
    """Return an explainable minimum-sufficient architecture recommendation."""
    reasons: list[str] = []
    alternatives: list[str] = ["deterministic_software", "llm_application", "rag", "agent_or_workflow"]

    if not req.needs_generation:
        return {
            "recommended_pattern": "deterministic_software",
            "alternatives_considered": alternatives,
            "reasons": ["generation is not required"],
        }

    if not req.needs_knowledge and not req.needs_actions:
        return {
            "recommended_pattern": "llm_application",
            "alternatives_considered": alternatives,
            "reasons": ["generation is required but external knowledge and actions are not"],
        }

    if req.needs_actions:
        pattern = "agent_or_workflow"
        reasons.append("the system must take or prepare actions")
        if req.roles > 3 and req.risk != Risk.HIGH:
            pattern = "evaluate_multi_agent"
            reasons.append("multiple independent roles may justify orchestration; benchmark against a single agent first")
        if req.risk == Risk.HIGH:
            reasons.append("high-risk actions require deterministic policy controls and approval boundaries")
        if req.human_approval:
            reasons.append("human approval is an explicit control boundary")
        return {
            "recommended_pattern": pattern,
            "alternatives_considered": alternatives + (["multi_agent"] if pattern == "evaluate_multi_agent" else []),
            "reasons": reasons,
            "complexity_warning": "prefer the simplest architecture that meets measured requirements",
        }

    if req.needs_knowledge:
        return {
            "recommended_pattern": "rag",
            "alternatives_considered": alternatives,
            "reasons": ["external, private, or changing knowledge is required at runtime"],
        }

    return {
        "recommended_pattern": "llm_application",
        "alternatives_considered": alternatives,
        "reasons": ["no stronger architectural requirement was identified"],
    }


if __name__ == "__main__":
    example = Requirements(
        needs_generation=True,
        needs_knowledge=True,
        needs_actions=True,
        roles=2,
        risk=Risk.HIGH,
        human_approval=True,
    )
    print(recommend(example))
