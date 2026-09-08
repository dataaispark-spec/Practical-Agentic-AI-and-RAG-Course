import subprocess
import sys

import pytest

from app.vector_search import ExactVectorIndex, VectorRecord, cosine, deterministic_embedding, recall_at_k


def record(record_id: str, text: str, tenant: str = "t1") -> VectorRecord:
    return VectorRecord(record_id, text, deterministic_embedding(text), tenant, "demo-v1", "idx-v1")


def test_embedding_is_reproducible_and_normalized():
    vector = deterministic_embedding("refund policy")
    assert vector == deterministic_embedding("refund policy")
    assert cosine(vector, vector) == pytest.approx(1.0)


def test_embedding_is_stable_across_processes():
    code = "from app.vector_search import deterministic_embedding; print(deterministic_embedding('stable query'))"
    output = subprocess.check_output([sys.executable, "-c", code], text=True)
    assert output.strip() == str(deterministic_embedding("stable query"))


def test_cosine_rejects_dimension_mismatch():
    with pytest.raises(ValueError):
        cosine((1.0, 0.0), (1.0,))


def test_exact_search_ranks_similar_content():
    index = ExactVectorIndex()
    index.add([record("a", "refund payment policy"), record("b", "weather forecast")])
    results = index.search(deterministic_embedding("refund payment"), 1)
    assert results[0][0].record_id == "a"


def test_tenant_filter_is_applied_during_search():
    index = ExactVectorIndex()
    index.add([record("a", "refund policy", "A"), record("b", "refund policy", "B")])
    results = index.search(deterministic_embedding("refund policy"), 1, tenant_id="B")
    assert [item[0].record_id for item in results] == ["b"]


def test_tie_break_is_deterministic():
    index = ExactVectorIndex()
    index.add([record("b", "same"), record("a", "same")])
    assert [x[0].record_id for x in index.search(deterministic_embedding("same"), 2)] == ["a", "b"]


def test_recall_at_k_uses_all_labeled_relevant_ids():
    assert recall_at_k(["a", "b", "c"], ["c", "a", "x"], 3) == pytest.approx(2 / 3)
