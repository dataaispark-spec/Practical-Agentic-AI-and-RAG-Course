import pytest

from app.router import Budget, BudgetExceeded, Requirements, Route, choose, cost_per_success, feasible, retry_amplification


def routes():
    return [Route('small',.80,400,.02),Route('medium',.90,800,.08),Route('large',.97,1400,.30,capabilities=frozenset({'reasoning'}))]


def test_feasibility():
    assert feasible(routes()[1],Requirements(.85,1000,.10))
    assert not feasible(routes()[0],Requirements(.85,1000,.10))


def test_choose_lowest_feasible_route():
    assert choose(routes(),Requirements(.85,1000,.10)).name=='medium'


def test_capability_constraint():
    assert choose(routes(),Requirements(.95,2000,.50,frozenset({'reasoning'}))).name=='large'


def test_no_feasible_route():
    try: choose(routes(),Requirements(.99,1000,1))
    except BudgetExceeded: pass
    else: raise AssertionError('expected no feasible route')


def test_budget():
    b=Budget(.10); b.reserve(.08)
    try: b.reserve(.03)
    except BudgetExceeded: pass
    else: raise AssertionError('expected budget failure')


def test_cost_per_success():
    assert cost_per_success(1.0,4)==.25


def test_retry_cost():
    assert retry_amplification(3,.1)==pytest.approx(.3)
