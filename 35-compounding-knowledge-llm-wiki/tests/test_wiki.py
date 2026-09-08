from app.wiki import Wiki, Claim

def test_upsert_and_provenance():
    w=Wiki(); w.upsert(Claim('rag','GraphRAG uses graph evidence','src-1'))
    assert 'src-1' in w.page('rag')

def test_unknown_is_explicit():
    assert Wiki().page('missing') == 'UNKNOWN'
