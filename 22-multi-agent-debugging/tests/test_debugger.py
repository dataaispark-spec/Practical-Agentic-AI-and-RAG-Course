from app.debugger import Failure, FailureClass, TraceDebugger, TraceEvent, validate_trace


def events():
    return [
        TraceEvent('e1','r1',None,None,'run.started','orchestrator',1.0),
        TraceEvent('e2','r1','e1','e1','agent.decided','supervisor',2.0,{'worker':'research'}),
        TraceEvent('e3','r1','e2','e2','retrieval.completed','retriever',3.0,{'index_version':'old'}),
        TraceEvent('e4','r1','e2','e3','verification.failed','verifier',4.0),
    ]


def test_causal_chain():
    d=TraceDebugger(events())
    assert [e.event_id for e in d.causal_chain('e4')]==['e1','e2','e3','e4']


def test_first_failure_is_earliest_event():
    d=TraceDebugger(events())
    failures=[Failure('e4',FailureClass.MODEL,'bad answer'),Failure('e3',FailureClass.RETRIEVAL,'stale index')]
    assert d.first_failure(failures).event_id=='e3'


def test_cost_attribution():
    es=events()+[TraceEvent('e5','r1','e4','e4','tool.completed','tool',5,{'cost_usd':.25})]
    assert d:=TraceDebugger(es)
    assert d.cost_by_component()['tool']==.25


def test_security_events():
    es=events()+[TraceEvent('e5','r1','e2','e2','security.denied','policy',5,{'security':True})]
    assert len(TraceDebugger(es).security_events())==1


def test_trace_validation():
    assert validate_trace(events())==[]
    broken=events()+[TraceEvent('bad','r1',None,'missing','tool.completed','tool',6)]
    assert validate_trace(broken)


def test_trace_diff():
    a=TraceDebugger(events())
    b=TraceDebugger(events()[:-1])
    assert b.trace_diff(a)
