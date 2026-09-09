from 36_loop_engineering.app.loop_engine import *


def test_action_id_is_stable():
    proposal = Proposal("read", {"resource": "x"})
    assert stable_action_id("t1", proposal) == stable_action_id("t1", proposal)


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

    engine = LoopEngine(observer, decider, policy, actor, verifier)
    out = engine.run(LoopState(Task("t1", "tenant-a", "test", max_steps=3)))
    assert out.result == "policy_denied"
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


def test_budget_stop_is_deterministic():
    calls = {"observe": 0}

    def observer(state):
        calls["observe"] += 1
        return Observation(f"o{calls['observe']}", "fake", {}, state.state_version + 1)

    def decider(state, obs):
        return Proposal("noop", {})

    def policy(state, proposal):
        return True, "allowed"

    def actor(state, proposal, action_id):
        return {"status": "not_done"}

    def verifier(state, proposal, result):
        return False

    out = LoopEngine(observer, decider, policy, actor, verifier).run(
        LoopState(Task("t3", "tenant-a", "loop", max_steps=2, max_repeated_states=99))
    )
    assert out.phase == Phase.STOP
    assert out.result == "safe_stop"
    assert out.stop_reason == "max_steps"
