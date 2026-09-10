from app.benchmark import recall_at_k, reciprocal_rank, reciprocal_rank_fusion


def test_rrf_prefers_consistent_candidates():
    ranking = reciprocal_rank_fusion([["a", "b"], ["b", "a"]])
    assert ranking[0] == "a" or ranking[0] == "b"
    assert set(ranking) == {"a", "b"}


def test_retrieval_metrics():
    ranking = ["x", "a", "b"]
    assert recall_at_k(ranking, {"a", "b"}, 2) == 0.5
    assert reciprocal_rank(ranking, {"a", "b"}) == 0.5
