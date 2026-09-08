from app.hybrid import rrf, hybrid

def test_rrf_fuses_rankings():
    hits=rrf(['a','b'],['b','c'])
    assert hits[0].item_id in {'a','b'}

def test_top_k():
    assert len(hybrid(['a','b','c'],['c','d','e'],2))==2
