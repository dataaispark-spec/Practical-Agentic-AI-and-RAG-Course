from app.core.contracts import ActionClass, ActionRequest, RiskLevel, TaskContract
from app.core.loop import BoundedAgentLoop, RunContext, RunState
from app.core.policy import PolicyEngine


def task(**overrides):
    values = dict(
        task_id="t1",
        goal="complete test task",
        owner="learner",
        tenant="demo",
        risk_level=RiskLevel.MEDIUM,
        allowed_systems=("crm.read", "crm.write"),
    )
    values.update(overrides)
    return TaskContract(**values)


def test_policy_allows_scoped_read():
    action = ActionRequest("a1", "t1", "crm.read", ActionClass.READ)
    decision = PolicyEngine().evaluate(task(), action)
    assert decision.allowed
    assert not decision.approval_required


def test_policy_rejects_out_of_scope_tool():
    action = ActionRequest("a1", "t1", "payments.write", ActionClass.WRITE)
    decision = PolicyEngine().evaluate(task(), action)
    assert not decision.allowed


def test_policy_gates_financial_action():
    action = ActionRequest("a1", "t1", "crm.write", ActionClass.FINANCIAL)
    decision = PolicyEngine().evaluate(task(), action)
    assert decision.allowed
    assert decision.approval_required


def test_loop_stops_when_verified():
    calls = {"observe": 0, "act": 0}

    def observe(ctx):
        calls["observe"] += 1
        return {"ready": True}

    def decide(ctx, observation):
        return "complete" if observation["ready"] else None

    def act(ctx, action):
        calls["act"] += 1
        return {"status": "ok"}

    def verify(ctx, result):
        return result["status"] == "ok"

    result = BoundedAgentLoop(observe, decide, act, verify).run(RunContext("t1", max_steps=3))
    assert result.state == RunState.COMPLETED
    assert result.step == 1
    assert calls == {"observe": 1, "act": 1}


def test_loop_has_hard_step_bound():
    def observe(ctx):
        return None

    def decide(ctx, observation):
        return "retry"

    def act(ctx, action):
        return None

    def verify(ctx, result):
        return False

    result = BoundedAgentLoop(observe, decide, act, verify).run(RunContext("t1", max_steps=3))
    assert result.state == RunState.FAILED
    assert result.step == 3
