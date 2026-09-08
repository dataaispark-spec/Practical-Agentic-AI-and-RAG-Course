from app.retrieval import Doc, bm25, dense, rrf, filter_metadata, secure_hybrid_retrieve, rerank, recall_at_k, mrr

DOCS = [
    Doc("d1", "CICS transaction timeout APAR PH12345 requires region restart.", {"tenant":"bank-a","version":"v2"}),
    Doc("d2", "Restart the CICS region after correcting timeout configuration.", {"tenant":"bank-a","version":"v2"}),
    Doc("d3", "AWS IAM troubleshooting for an expired access key.", {"tenant":"cloud-a","version":"v1"}),
]


def test_lexical_finds_identifier():
    hits = bm25(DOCS, "PH12345", 2)
    assert hits[0].doc_id == "d1"


def test_dense_returns_ranked_results():
    hits = dense(DOCS, "CICS timeout", 2)
    assert len(hits) == 2


def test_rrf_combines_lists():
    a = bm25(DOCS, "CICS timeout", 3)
    b = dense(DOCS, "transaction timeout", 3)
    hits = rrf(a, b, limit=3)
    assert hits and hits[0].doc_id in {"d1", "d2"}


def test_metadata_filter():
    hits = dense(DOCS, "timeout", 3)
    filtered = filter_metadata(hits, DOCS, {"tenant":"bank-a"})
    assert all(h.doc_id in {"d1", "d2"} for h in filtered)


def test_secure_hybrid_filters_before_candidate_truncation():
    hits = secure_hybrid_retrieve(DOCS, "CICS timeout", {"tenant":"bank-a"}, candidate_k=2, limit=2)
    assert {h.doc_id for h in hits} <= {"d1", "d2"}
    assert hits


def test_reranker_preserves_candidate_pool():
    hits = rrf(bm25(DOCS, "CICS", 3), dense(DOCS, "CICS", 3), limit=3)
    ranked = rerank(hits, DOCS, "CICS transaction timeout", 2)
    assert len(ranked) == 2


def test_metrics():
    ranked = bm25(DOCS, "PH12345", 3)
    assert recall_at_k(ranked, {"d1"}, 1) == 1.0
    assert mrr(ranked, {"d1"}) == 1.0
