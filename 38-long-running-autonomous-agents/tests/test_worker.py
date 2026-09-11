from app.worker import Budget, DurableJob, DurableStore, DurableWorker, Status, retry_amplification
import pytest


def test_resume_after_crash_does_not_duplicate_external_effect():
    calls = []
    worker = DurableWorker(lambda effect_id: calls.append(effect_id) or effect_id)
    job = DurableJob("j", "reconcile", total_steps=3)

    worker.run(job, steps=3, crash_after_effect_at=1)
    assert calls == ["j:effect:0", "j:effect:1"]
    assert job.checkpoint == 1

    job.status = Status.CREATED
    worker.run(job, steps=3)
    assert calls == ["j:effect:0", "j:effect:1", "j:effect:2"]
    assert job.completed_effect_ids == {"j:effect:0", "j:effect:1", "j:effect:2"}
    assert job.status is Status.COMPLETED


def test_fencing_rejects_stale_worker():
    store = DurableStore()
    job = DurableJob("j", "goal", total_steps=1)
    store.put(job)
    first = store.acquire_lease("j", "A", now=0, ttl=2)
    store.acquire_lease("j", "B", now=3, ttl=2)
    with pytest.raises(RuntimeError, match="stale worker"):
        store.commit_checkpoint("j", "A", first.fence, now=3, checkpoint=1)


def test_expired_lease_is_rejected():
    store = DurableStore()
    job = DurableJob("j", "goal")
    store.put(job)
    lease = store.acquire_lease("j", "A", now=0, ttl=2)
    with pytest.raises(RuntimeError, match="expired lease"):
        store.renew_lease("j", "A", lease.fence, now=2)


def test_wait_resume_and_cancel_are_durable_states():
    worker = DurableWorker(lambda effect_id: effect_id)
    job = DurableJob("j", "approval", total_steps=1)
    worker.wait(job, "human approval")
    assert job.status is Status.WAITING
    assert job.wait_reason == "human approval"
    worker.resume(job)
    assert job.status is Status.CREATED and job.wait_reason is None
    worker.cancel(job)
    assert job.status is Status.CANCELLED


def test_approval_is_bound_to_action_and_policy_version():
    worker = DurableWorker(lambda effect_id: effect_id)
    job = DurableJob("j", "disable account")
    worker.bind_approval(job, "hash-v1", "policy-7")
    assert worker.authorize(job, "hash-v1", "policy-7")
    assert not worker.authorize(job, "hash-v2", "policy-7")
    assert not worker.authorize(job, "hash-v1", "policy-8")


def test_budget_is_cumulative_and_bounded():
    budget = Budget(max_steps=2, max_tool_calls=2, max_cost=0.2)
    budget.spend(steps=1, tool_calls=1, cost=0.1)
    assert budget.can_spend(steps=1, tool_calls=1, cost=0.1)
    with pytest.raises(RuntimeError, match="budget exhausted"):
        budget.spend(steps=1, tool_calls=1, cost=0.1001)


def test_retry_amplification_is_explicit():
    assert retry_amplification(10, retries=2, fanout=2) == 70


def test_checkpoint_never_moves_backward():
    store = DurableStore()
    job = DurableJob("j", "goal")
    store.put(job)
    lease = store.acquire_lease("j", "A", now=0)
    store.commit_checkpoint("j", "A", lease.fence, now=0, checkpoint=3)
    with pytest.raises(RuntimeError, match="checkpoint regression"):
        store.commit_checkpoint("j", "A", lease.fence, now=0, checkpoint=2)


def test_reconciliation_closes_timeout_after_write_without_duplicate_call():
    calls = []
    worker = DurableWorker(lambda effect_id: calls.append(effect_id) or "external-write")
    job = DurableJob("j", "goal", total_steps=1)
    # Model a timeout where the external system actually applied the effect.
    job.effects["j:effect:0"] = worker.store.get(job.job_id).effects["j:effect:0"] if job.job_id in worker.store.jobs else None
    job.effects.pop("j:effect:0", None)
    job.effects["j:effect:0"] = __import__("app.worker", fromlist=["EffectRecord"]).EffectRecord("j:effect:0", status="unknown")
    worker.reconcile(job, "j:effect:0", "confirmed-by-ledger")
    job.status = Status.CREATED
    worker.run(job, steps=1)
    assert calls == []
    assert job.completed_effect_ids == {"j:effect:0"}
