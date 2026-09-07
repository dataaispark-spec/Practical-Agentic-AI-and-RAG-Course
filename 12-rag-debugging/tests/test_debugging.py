from app.debugging import Trace, classify

def test_first_failure():
    t=Trace('r1'); t.record('retrieval',status='ok'); t.record('ranking',status='error',error_type='ValueError')
    assert t.first_failure()['stage']=='ranking'
    assert classify(t)=='ranking_failure'

def test_no_failure():
    t=Trace('r2'); t.record('generation',status='ok')
    assert classify(t)=='no_observed_failure'

def test_filter_failure_classification():
    t=Trace('r3'); t.record('filter',status='error')
    assert classify(t)=='authorization_or_metadata_failure'
