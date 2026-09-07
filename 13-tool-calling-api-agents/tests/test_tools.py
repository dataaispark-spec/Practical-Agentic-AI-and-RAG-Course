import pytest
from app.tools import Tool, ToolRegistry, Risk, PolicyDenied, ApprovalRequired

def test_read_tool():
    r=ToolRegistry(); r.register(Tool('lookup',lambda customer_id:f'customer:{customer_id}','support',Risk.READ))
    assert r.call('lookup',role='support',args={'customer_id':'C1'})=='customer:C1'

def test_policy_denied():
    r=ToolRegistry(); r.register(Tool('lookup',lambda:'ok','support',Risk.READ))
    with pytest.raises(PolicyDenied): r.call('lookup',role='guest')

def test_approval_gate():
    r=ToolRegistry(); r.register(Tool('refund',lambda amount:f'refund:{amount}','finance',Risk.HIGH_IMPACT))
    with pytest.raises(ApprovalRequired): r.call('refund',role='finance',args={'amount':10})
    assert r.call('refund',role='finance',approved=True,args={'amount':10})=='refund:10'

def test_idempotency():
    calls=[]
    r=ToolRegistry(); r.register(Tool('write',lambda: calls.append(1) or 'ok','ops',Risk.WRITE))
    assert r.call('write',role='ops',idempotency_key='k')=='ok'
    assert r.call('write',role='ops',idempotency_key='k')=='ok'
    assert len(calls)==1
