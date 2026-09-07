import time
import pytest
from app.coordination import CoordinationError, FailureClass, Message, TaskCoordinator, TaskStatus, backoff, expired


def test_lease_and_stale_worker_rejection():
    c=TaskCoordinator(lease_seconds=60)
    t=c.create('tenant-a'); lease=c.claim(t.task_id,'w1')
    with pytest.raises(CoordinationError): c.claim(t.task_id,'w2')
    c.complete(t.task_id,lease,'ok')
    assert t.status==TaskStatus.COMPLETED
    with pytest.raises(CoordinationError): c.complete(t.task_id,lease,'duplicate')


def test_heartbeat_requires_current_lease():
    c=TaskCoordinator(); t=c.create('t'); lease=c.claim(t.task_id,'w')
    c.heartbeat(t.task_id,lease)
    with pytest.raises(CoordinationError): c.heartbeat(t.task_id,'stale')


def test_expired_lease_becomes_recoverable():
    c=TaskCoordinator(lease_seconds=0); t=c.create('t'); c.claim(t.task_id,'w')
    time.sleep(0.001)
    assert t.task_id in c.expire_leases()
    assert t.status==TaskStatus.RECOVERABLE


def test_idempotent_side_effect():
    c=TaskCoordinator()
    assert c.record_effect('k1','done')
    assert not c.record_effect('k1','done-again')


def test_retryable_vs_permanent_failure():
    c=TaskCoordinator(max_attempts=2); t=c.create('t'); c.claim(t.task_id,'w')
    assert c.retry_or_dead_letter(t.task_id,FailureClass.TRANSIENT)==TaskStatus.PENDING
    c.claim(t.task_id,'w'); assert c.retry_or_dead_letter(t.task_id,FailureClass.TRANSIENT)==TaskStatus.DEAD_LETTER


def test_backoff_increases():
    assert backoff(2,base=1,jitter=0)==2
    assert backoff(4,base=1,jitter=0)==8


def test_message_expiry():
    m=Message('m','c',None,'a','b','t','v1',{},'k',expires_at=10)
    assert expired(m,now=11)
    assert not expired(m,now=9)


def test_cancel():
    c=TaskCoordinator(); t=c.create('t'); c.cancel(t.task_id)
    assert t.status==TaskStatus.CANCELLED
    with pytest.raises(CoordinationError): c.claim(t.task_id,'w')
