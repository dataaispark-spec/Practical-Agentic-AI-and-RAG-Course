import time
import pytest
from app.runtime import ContractError, SupervisorRuntime, TaskEnvelope, Worker, WorkerRegistry, WorkerResult


class Research(Worker):
    name='research'; capabilities=frozenset({'kb:read'})
    def run(self, task): return WorkerResult(task.task_id,self.name,['source'],.9)

class Finance(Worker):
    name='finance'; capabilities=frozenset({'finance:write'})
    def run(self, task): return WorkerResult(task.task_id,self.name,['approved evidence'],.8)


def runtime(): return SupervisorRuntime(WorkerRegistry([Research(),Finance()]))


def test_capability_contract():
    r=runtime(); t=r.envelope(tenant_id='t1',worker='research',capabilities=frozenset({'kb:read'}),payload={})
    assert r.dispatch(t).ok
    with pytest.raises(ContractError):
        r.envelope(tenant_id='t1',worker='research',capabilities=frozenset({'finance:write'}),payload={}) and r.dispatch(t)


def test_result_contract():
    r=runtime(); r.validate_result(WorkerResult('1','research',True,['e'],.5))
    with pytest.raises(ContractError): r.validate_result(WorkerResult('1','research',True,[],.5))


def test_duplicate_dispatch_is_deduplicated():
    r=runtime(); t=r.envelope(tenant_id='t1',worker='research',capabilities=frozenset({'kb:read'}),payload={})
    first=r.dispatch(t); second=r.dispatch(t)
    assert first.ok and second.evidence==['deduplicated']


def test_expired_task_fails():
    r=runtime(); t=TaskEnvelope('x',None,'t1','research',frozenset({'kb:read'}),{},time.monotonic()-1,'k')
    assert not r.dispatch(t).ok


def test_fan_out():
    r=runtime(); tasks=[r.envelope(tenant_id='t1',worker='research',capabilities=frozenset({'kb:read'}),payload={'i':i}) for i in range(3)]
    results=r.fan_out(tasks)
    assert len(results)==3 and all(x.ok for x in results)
