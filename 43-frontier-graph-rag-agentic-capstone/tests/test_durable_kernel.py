from pathlib import Path

import pytest

from app.core.budget import Budget, BudgetExceeded
from app.core.durable import DurableRunStore, RunStatus
from app.core.audit import AuditLog


def test_run_survives_reload(tmp_path: Path):
    store = DurableRunStore(tmp_path / "runs")
    run = store.create("task-1", {"stage": "observe"})
    run.status = RunStatus.RUNNING
    run.state["answer"] = "checkpointed"
    store.checkpoint(run)

    recovered = store.load(run.run_id)
    assert recovered.status is RunStatus.RUNNING
    assert recovered.state["answer"] == "checkpointed"
    assert recovered.sequence == 1


def test_idempotency_key_blocks_duplicate_action(tmp_path: Path):
    store = DurableRunStore(tmp_path / "runs")
    run = store.create("task-1")
    assert store.mark_idempotency_key(run, "send:123") is True
    assert store.mark_idempotency_key(run, "send:123") is False


def test_cancel_persists(tmp_path: Path):
    store = DurableRunStore(tmp_path / "runs")
    run = store.create("task-1")
    store.cancel(run)
    assert store.load(run.run_id).status is RunStatus.CANCELLED


def test_budget_is_multidimensional():
    budget = Budget(max_steps=1, max_tokens=10, max_tool_calls=1, max_cost_usd=1.0)
    budget.consume_step()
    with pytest.raises(BudgetExceeded):
        budget.consume_step()


def test_audit_log_is_reconstructable(tmp_path: Path):
    audit = AuditLog(tmp_path / "audit.jsonl")
    audit.record("run-1", 1, "ACTION", tool="search", result="ok")
    audit.record("run-2", 1, "ACTION", tool="other")
    events = audit.for_run("run-1")
    assert len(events) == 1
    assert events[0].data["tool"] == "search"
