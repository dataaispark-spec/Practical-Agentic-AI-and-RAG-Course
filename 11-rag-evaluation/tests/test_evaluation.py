from app.evaluation import recall_at_k, reciprocal_rank, exact_match, groundedness, regression_gate, bootstrap_mean

def test_recall():
    assert recall_at_k(['a','b','c'], {'b'}, 2) == 1.0

def test_mrr():
    assert reciprocal_rank(['x','b','c'], {'b'}) == 0.5

def test_exact_match():
    assert exact_match(' Answer ', 'answer') == 1.0

def test_groundedness():
    assert groundedness(['a','b'], ['a','x']) == 0.5

def test_regression_gate():
    assert regression_gate(0.90, 0.89)
    assert not regression_gate(0.90, 0.87)

def test_bootstrap_is_bounded():
    lo, hi = bootstrap_mean([0,1,1,1], iterations=100)
    assert 0 <= lo <= hi <= 1
