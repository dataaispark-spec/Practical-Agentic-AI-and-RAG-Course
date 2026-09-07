from app.governance import Decision, GovernancePolicy, UseCase, action_hash, evaluate

P = GovernancePolicy(frozenset({'model-a'}), frozenset({'search'}))


def test_allow_low_risk():
    d=evaluate(UseCase('1','t1','faq',1,'internal','model-a','search'),P)
    assert d.decision is Decision.ALLOW


def test_model_denied():
    d=evaluate(UseCase('1','t1','faq',1,'internal','model-b','search'),P)
    assert d.decision is Decision.DENY and d.reason=='model_not_approved'


def test_data_denied():
    d=evaluate(UseCase('1','t1','faq',1,'restricted','model-a','search'),P)
    assert d.decision is Decision.DENY


def test_tool_denied():
    d=evaluate(UseCase('1','t1','faq',1,'internal','model-a','delete'),P)
    assert d.decision is Decision.DENY


def test_high_risk_requires_approval():
    d=evaluate(UseCase('1','t1','payment',3,'internal','model-a','search',True),P)
    assert d.decision is Decision.APPROVAL_REQUIRED


def test_high_risk_without_oversight_denied():
    d=evaluate(UseCase('1','t1','payment',3,'internal','model-a','search',False),P)
    assert d.decision is Decision.DENY


def test_hash_is_stable_and_action_bound():
    a=UseCase('1','t1','faq',1,'internal','model-a','search')
    b=UseCase('1','t1','faq',2,'internal','model-a','search')
    assert action_hash(a)==action_hash(a)
    assert action_hash(a)!=action_hash(b)
