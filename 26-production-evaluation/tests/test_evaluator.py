from app.evaluator import EvalCase, EvalResult, Gate, bootstrap_delta, gate, score_case, summarize


def test_score_success_and_evidence():
    c=EvalCase('1','q','approved',required_evidence=('doc1',),forbidden=('unsafe',))
    r=score_case(c,'approved response',evidence=['doc1'],cost_usd=.2,latency_ms=10)
    assert r.success and r.safety and r.quality==1.0


def test_forbidden_output_fails_safety():
    c=EvalCase('1','q','ok',forbidden=('delete',))
    assert not score_case(c,'delete this',evidence=[]).safety


def test_summary():
    rs=[EvalResult('1',True,.9,True,.2,10),EvalResult('2',False,.4,True,.3,20)]
    m=summarize(rs)
    assert m['success_rate']==.5 and m['cost_per_success']==.5


def test_gate_blocks_safety():
    rs=[EvalResult('1',True,1,False)]
    ok, failures=gate(rs,Gate(min_success=.9,min_quality=.8))
    assert not ok and 'safety' in failures


def test_gate_passes():
    rs=[EvalResult('1',True,1,True,.1,10),EvalResult('2',True,.9,True,.1,12)]
    ok, failures=gate(rs,Gate(min_success=.9,min_quality=.8,max_cost_per_success=.2,max_latency_ms=20))
    assert ok and not failures


def test_paired_delta_interval_contains_mean():
    mean, interval=bootstrap_delta([1,2,3],[0,1,2])
    assert mean==1 and interval[0] <= mean <= interval[1]
