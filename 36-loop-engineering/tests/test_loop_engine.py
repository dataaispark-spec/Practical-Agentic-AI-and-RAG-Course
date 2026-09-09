from importlib import import_module

m = import_module("36-loop-engineering.app.loop_engine")
LoopEngine = m.LoopEngine
LoopState = m.LoopState
Observation = m.Observation
Outcome = m.Outcome
Phase = m.Phase
Proposal = m.Proposal
Task = m.Task
stable_action_id = m.stable_action_id
stop_if_budget_exhausted = m.stop_if_budget_exhausted


def test_action_id_is_stable_and_changes_with_arguments():
    p1 = Proposal("read", {"resource": "x"})
    p2 = Proposal("read", {"resource": "y"})
    assert stable_action_id("t1", p1) == stable_action_id("t1", p1)
    assert stable_action_id("t1", p1) != stable_action_id("t1", p2)


def test_policy_deny_stops_without_actor():
    calls = {"actor": 0}

    def observer(state):
        return Observation("o1", "fake", {"ok": True}, state.state_version + 1)

    def decider(state, obs):
        return Proposal("danger", {"tenant": "other"})

    def policy(state, proposal):
        return False, "tenant_mismatch"

    def actor(state, proposal, action_id):
        calls["actor"] += 1
        return {"ok": True}

    def verifier(state, proposal, result):
        return True

    out = LoopEngine(observer, decider, policy, actor, verifier).run(
        LoopState(Task("t1", "tenant-a", "test", max_steps=3))
    )
    assert out.result == "policy_denied"
    assert out.phase == Phase.ESCALATE
    assert calls["actor"] == 0


def test_success_records_verified_action():
    executed = []

    def observer(state):
        return Observation("o1", "fake", {"ready": True}, state.state_version + 1)

    def decider(state, obs):
        return Proposal("safe_read", {"resource": "r1"})

    def policy(state, proposal):
        return True, "allowed"

    def actor(state, proposal, action_id):
        executed.append(action_id)
        return {"status": "ok"}

    def verifier(state, proposal, result):
        return result.get("status") == "ok"

    out = LoopEngine(observer, decider, policy, actor, verifier).run(
        LoopState(Task("t2", "tenant-a", "read", max_steps=2))
    )
    assert out.result == "verified_success"
    assert out.verified is True
    assert len(executed) == 1
    assert out.phase == Phase.COMPLETE


def test_budget_boundary_is_deterministic():
    state = LoopState(
        Task("t3", "tenant-a", "loop", max_steps=2, max_repeated_states=99),
        step=2,
    )
    assert stop_if_budget_exhausted(state) is None
    state.step = 3
    assert stop_if_budget_exhausted(state) == "max_steps"


def test_stale_observation_recovers_then_succeeds():
    observations = iter([
        Observation("stale", "fake", {}, 1, fresh=False),
        Observation("fresh", "fake", {"ready": True}, 2, fresh=True),
    ])

    def observer(state):
        return next(observations)

    def decider(state, obs):
        return Proposal("read", {"resource": "r"})

    def policy(state, proposal):
        return True, "allowed"

    def actor(state, proposal, action_id):
        return {"status": "ok"}

    def verifier(state, proposal, result):
        return result["status"] == "ok"

    out = LoopEngine(observer, decider, policy, actor, verifier).run(
        LoopState(Task("t4", "tenant-a", "recover", max_steps=4))
    )
    assert out.result == "verified_success"
    assert any(e.phase == Phase.RECOVER for e in out.trace)


def test_repeated_verification_failure_escalates():
    def observer(state):
        return Observation(f"o{state.step}", "fake", {"ready": True}, state.state_version + 1)

    def decider(state, obs):
        return Proposal("noop", {})

    def policy(state, proposal):
        return True, "allowed"

    def actor(state, proposal, action_id):
        return {"status": "not_done"}

    def verifier(state, proposal, result):
        return False

    def recover(state, reason):
        return Outcome.ESCALATE

    out = LoopEngine(observer, decider, policy, actor, verifier, recover=recover).run(
        LoopState(Task("t5", "tenant-a", "verify", max_steps=5))
    )
    assert out.phase == Phase.ESCALATE
    assert out.result == "human_escalation"


def test_duplicate_action_is_not_executed_twice():
    executed = []

    def observer(state):
        return Observation(f"o{state.step}", "fake", {"ready": True}, state.state_version + 1)

    def decider(state, obs):
        return Proposal("read", {"resource": "r"})

    def policy(state, proposal):
        return True, "allowed"

    def actor(state, proposal, action_id):
        executed.append(action_id)
        return {"status": "ok"}

    def verifier(state, proposal, result):
        return True

    state = LoopState(Task("t6", "tenant-a", "dedupe", max_steps=1))
    action_id = stable_action_id(state.task.task_id, Proposal("read", {"resource": "r"}))
    state.completed_action_ids.add(action_id)
    out = LoopEngine(observer, decider, policy, actor, verifier).run(state)
    assert out.result == "verified_success"
    assert executed == []
