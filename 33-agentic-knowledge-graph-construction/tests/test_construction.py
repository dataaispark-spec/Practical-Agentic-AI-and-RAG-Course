from app.construction import Proposal, validate, commit

def test_validation_requires_evidence_and_confidence():
    assert validate(Proposal('a','OWNS','b','s',.9), {'a','b'})
    assert not validate(Proposal('a','OWNS','b','',.9), {'a','b'})
    assert not validate(Proposal('a','OWNS','x','s',.9), {'a','b'})

def test_commit_deduplicates():
    p=Proposal('a','OWNS','b','s',.9)
    assert len(commit([p,p], {'a','b'})) == 1
