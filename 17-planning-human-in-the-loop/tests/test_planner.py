import pytest
from app.planner import *

def test_dag_execution():
    p=Plan('p',[PlanStep('a','collect'),PlanStep('b','analyze',('a',))])
    out=PlannerExecutor(lambda s:s.objective,lambda s,r:True).run('t',p)
    assert out==['collect','analyze']

def test_cycle_rejected():
    p=Plan('p',[PlanStep('a','x',('b',)),PlanStep('b','y',('a',))])
    with pytest.raises(PlanError): validate_plan(p)

def test_exact_approval_required():
    s=PlanStep('pay','pay vendor',risk=Risk.HIGH,tool='payment')
    p=Plan('p',[s]); good=Approval('t',action_hash('t',s),'alice',True)
    assert PlannerExecutor(lambda s:'ok',lambda s,r:True).run('t',p,{'pay':good})==['ok']
    with pytest.raises(PermissionError): PlannerExecutor(lambda s:'ok',lambda s,r:True).run('t',p)
