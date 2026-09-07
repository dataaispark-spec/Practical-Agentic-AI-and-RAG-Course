from app.capstone import CapstoneTask, Phase, RunState, stable_action_id, verify_completion


def task():
    return CapstoneTask('case-1','tenant-a','investigate case',2,1.0,frozenset({'search'}))


def test_initial_governance_phase():
    assert RunState(task()).phase is Phase.GOVERN


def test_budget_is_hard():
    s=RunState(task()); s.consume(.7)
    try: s.consume(.4)
    except RuntimeError: pass
    else: raise AssertionError('expected budget failure')


def test_action_id_is_stable_and_tenant_bound():
    assert stable_action_id(task(),'search')==stable_action_id(task(),'search')
    other=CapstoneTask('case-1','tenant-b','investigate case',2,1.0,frozenset({'search'}))
    assert stable_action_id(task(),'search')!=stable_action_id(other,'search')


def test_completion_requires_evidence():
    s=RunState(task()); assert not verify_completion(s)
    s.evidence.append('policy-doc-17'); assert verify_completion(s)
