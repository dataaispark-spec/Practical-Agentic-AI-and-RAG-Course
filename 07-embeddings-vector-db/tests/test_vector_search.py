from app.vector_search import ExactVectorIndex, VectorRecord, cosine, deterministic_embedding, recall_at_k


def record(record_id: str, text: str, tenant: str = "t1") -> VectorRecord:
    return VectorRecord(record_id, text, deterministic_embedding(text), tenant, "demo-v1", "idx-v1")


def test_embedding_is_normalized_for_non_empty_text():
    vector = deterministic_embedding("refund policy")
    assert abs(cosine(vector, vector) - 1.0) < 1e-9


def test_exact_search_ranks_similar_content():
    index = ExactVectorIndex()
    index.add([record("a", "refund payment policy"), record("b", "weather forecast")])
    results = index.search(deterministic_embedding("refund payment"), 1)
    assert results[0][0].record_id == "a"


def test_tenant_filter_is_applied_during_search():
    index = ExactVectorIndex()
    index.add([record("a", "refund policy", "A"), record("b", "refund policy", "B")])
    results = index.search(deterministic_embedding("refund policy"), 10, tenant_id="A")
    assert [item[0].record_id for item in results] == ["a"]


def test_recall_at_k():
    assert recall_at_k(["a", "b", "c"], ["c", "a", "x"], 2) == 0.5
