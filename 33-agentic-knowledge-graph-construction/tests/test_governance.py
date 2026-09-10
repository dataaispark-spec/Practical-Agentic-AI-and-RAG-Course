import pytest

from app.governance import Proposal, approval_required, validate


def test_proposal_hash_is_stable():
    p = Proposal("A", "OWNS", "B", "src-1", "t1", 0.9)
    assert p.proposal_id == Proposal("A", "OWNS", "B", "src-1", "t1", 0.9).proposal_id


def test_validation_rejects_unknown_or_unsupported():
    with pytest.raises(ValueError):
        validate(Proposal("A", "BAD", "B", "src", "t1", 0.9), {"A", "B"}, {"OWNS"})


def test_high_risk_requires_approval():
    assert approval_required(Proposal("A", "OWNS", "B", "src", "t1", 0.9, "high"))
