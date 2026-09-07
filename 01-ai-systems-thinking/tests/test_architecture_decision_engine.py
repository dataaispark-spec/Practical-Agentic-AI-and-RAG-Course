from labs.architecture_decision_engine import Requirements, explain, recommend


def test_deterministic_is_preferred_when_generation_is_unnecessary():
    result = recommend(Requirements(needs_generation=False, needs_knowledge=True, needs_actions=True))
    assert result.recommended_pattern == "deterministic_software"


def test_simple_generation_uses_llm_application():
    result = recommend(Requirements(needs_generation=True, needs_knowledge=False, needs_actions=False))
    assert result.recommended_pattern == "llm_application"


def test_private_knowledge_selects_rag():
    result = recommend(Requirements(needs_generation=True, needs_knowledge=True, needs_actions=False))
    assert result.recommended_pattern == "rag"


def test_high_risk_action_requires_controlled_approval():
    result = recommend(Requirements(True, True, True, risk="high", human_approval=True))
    assert result.recommended_pattern == "rag_with_workflow_and_approval"
    assert "authorization" in result.complexity_warning.lower()


def test_many_roles_do_not_automatically_mean_multi_agent():
    result = recommend(Requirements(True, False, True, roles=4, risk="low"))
    assert result.recommended_pattern == "evaluate_multi_agent"


def test_explain_is_json_serializable_shape():
    result = explain(Requirements(True, True, False))
    assert set(result) == {
        "recommended_pattern",
        "alternatives_considered",
        "reasons",
        "complexity_warning",
    }
