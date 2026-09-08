from app.improvement import Candidate, ImprovementEngine

def candidate(): return Candidate('c1','v1','abc',{})

def test_safety_regression_blocks_promotion():
    e=ImprovementEngine(lambda c:{'success':.9,'safety':.8,'cost':.1}); e.set_baseline({'success':.8,'safety':1.0,'cost':.1})
    d=e.evaluate(candidate()); assert not d.promoted and 'safety_regression' in d.reasons

def test_success_gain_can_promote():
    e=ImprovementEngine(lambda c:{'success':.84,'safety':1.0,'cost':.1}); e.set_baseline({'success':.8,'safety':1.0,'cost':.1})
    assert e.evaluate(candidate()).promoted

def test_experiment_budget_is_hard():
    e=ImprovementEngine(lambda c:{'success':.84,'safety':1.0,'cost':.1},max_experiments=1); e.set_baseline({'success':.8,'safety':1.0,'cost':.1})
    e.evaluate(candidate()); assert not e.evaluate(Candidate('c2','v1','def',{})).promoted
