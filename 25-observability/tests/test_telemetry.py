from app.telemetry import Event, Metric, Span, TelemetryStore, critical_path, detect_retry_amplification, percentile


def span(i, parent, component, start, end, **attrs):
    return Span(i,"t1",parent,"tenant-a",component,component,start,end,attrs)


def test_trace_is_tenant_scoped_and_sorted():
    s=TelemetryStore(); s.add_span(span("b","a","tool",2,3)); s.add_span(span("a",None,"agent",1,4))
    s.add_span(Span("x","t1",None,"tenant-b","secret",0,99))
    assert [x.span_id for x in s.trace("t1","tenant-a")] == ["a","b"]


def test_cost_and_tokens():
    s=TelemetryStore(); s.add_span(span("a",None,"model",0,1,cost_usd=.3,tokens=100)); s.add_span(span("b","a","tool",1,2,cost_usd=.2,tokens=20))
    assert s.cost("t1","tenant-a")==.5
    assert s.token_count("t1","tenant-a")==120


def test_critical_path():
    ss=[span("a",None,"agent",0,1),span("b","a","model",1,3),span("c","b","tool",3,4)]
    assert critical_path(ss)==4000


def test_percentile():
    assert percentile([1,2,3,4,5],50)==3


def test_retry_amplification():
    ss=[span(str(i),None,"api","0","1",attempt=2) for i in range(3)]
    assert "api:api" in detect_retry_amplification(ss,3)


def test_events():
    s=TelemetryStore(); s.add_event(Event("e","t1","tenant-a","policy.denied",1))
    s.add_metric(Metric("task_success",1,"tenant-a"))
    assert s.events_for("t1","tenant-a")[0].event_type=="policy.denied"
