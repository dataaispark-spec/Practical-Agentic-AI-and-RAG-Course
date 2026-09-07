import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from architecture_decider import recommend
from models import Requirements, Risk


def test_deterministic_when_generation_not_needed() -> None:
    result = recommend(Requirements(False, False, False))
    assert result["recommended_pattern"] == "deterministic_software"


def test_llm_application() -> None:
    result = recommend(Requirements(True, False, False))
    assert result["recommended_pattern"] == "llm_application"


def test_rag() -> None:
    result = recommend(Requirements(True, True, False))
    assert result["recommended_pattern"] == "rag"


def test_agent_for_action() -> None:
    result = recommend(Requirements(True, False, True))
    assert result["recommended_pattern"] == "agent_or_workflow"


def test_high_risk_still_requires_controls() -> None:
    result = recommend(Requirements(True, True, True, risk=Risk.HIGH, human_approval=True))
    assert result["recommended_pattern"] == "agent_or_workflow"
    assert any("deterministic policy" in reason for reason in result["reasons"])


def test_multi_agent_is_only_an_evaluation_flag() -> None:
    result = recommend(Requirements(True, True, True, roles=5, risk=Risk.MEDIUM))
    assert result["recommended_pattern"] == "evaluate_multi_agent"
    assert "multi_agent" in result["alternatives_considered"]


def test_multi_agent_not_recommended_automatically_for_high_risk() -> None:
    result = recommend(Requirements(True, True, True, roles=8, risk=Risk.HIGH))
    assert result["recommended_pattern"] == "agent_or_workflow"


def test_human_approval_is_reflected() -> None:
    result = recommend(Requirements(True, False, True, human_approval=True))
    assert any("human approval" in reason for reason in result["reasons"])


def test_roles_must_be_positive() -> None:
    try:
        Requirements(True, False, False, roles=0)
    except ValueError as exc:
        assert "roles" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_reason_is_present_for_every_recommendation() -> None:
    cases = [
        Requirements(False, False, False),
        Requirements(True, False, False),
        Requirements(True, True, False),
        Requirements(True, True, True),
    ]
    for case in cases:
        result = recommend(case)
        assert result["reasons"]
