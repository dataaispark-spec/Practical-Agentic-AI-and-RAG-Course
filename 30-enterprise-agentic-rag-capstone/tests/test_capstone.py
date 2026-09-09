import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import AegisAI, Evidence, Task
from app.capstone import CapstoneTask, Phase, RunState, stable_action_id, verify_completion


def task():
    return CapstoneTask("case-1", "tenant-a", "investigate case", 2, 1.0, frozenset({"search"}))


def test_authorization_is_explicit():
    a = AegisAI()
    task_ = Task("investigate", "tenant-a", allowed_tools={"search"})
    assert a.authorize(task_, "search") is True
    assert a.authorize(task_, "refund") is False


def test_verification_requires_authorized_evidence():
    a = AegisAI()
    task_ = Task("investigate", "tenant-a")
    assert a.verify(task_, [Evidence("doc-1", "supported")]) is True
    task2 = Task("investigate", "tenant-a")
    assert a.verify(task2, [Evidence("doc-2", "bad", authorized=False)]) is False


def test_initial_governance_phase():
    assert RunState(task()).phase is Phase.GOVERN


def test_budget_is_hard():
    state = RunState(task())
    state.consume(0.7)
    try:
        state.consume(0.4)
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected budget failure")


def test_action_id_is_stable_and_tenant_bound():
    assert stable_action_id(task(), "search") == stable_action_id(task(), "search")
    other = CapstoneTask("case-1", "tenant-b", "investigate case", 2, 1.0, frozenset({"search"}))
    assert stable_action_id(task(), "search") != stable_action_id(other, "search")


def test_completion_requires_evidence():
    state = RunState(task())
    assert not verify_completion(state)
    state.evidence.append("policy-doc-17")
    assert verify_completion(state)
