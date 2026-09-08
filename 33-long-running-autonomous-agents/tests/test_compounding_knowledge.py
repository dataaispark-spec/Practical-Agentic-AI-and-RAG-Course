import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.compounding_knowledge import KnowledgeBase, KnowledgeItem


def test_compounding_update_does_not_duplicate():
    kb = KnowledgeBase()
    item = KnowledgeItem("k1", "A", "OWNS", "B", "source-1")
    assert kb.upsert(item) == "added"
    assert kb.upsert(item) == "duplicate"
    assert kb.health()["active"] == 1


def test_conflicting_evidence_is_recorded_not_silently_overwritten():
    kb = KnowledgeBase()
    assert kb.upsert(KnowledgeItem("k1", "A", "STATUS", "active", "s1")) == "added"
    assert kb.upsert(KnowledgeItem("k2", "A", "STATUS", "closed", "s2")) == "contradiction"
    assert kb.health()["contradictions"] == 1


def test_supersession_is_explicit():
    kb = KnowledgeBase()
    kb.upsert(KnowledgeItem("k1", "A", "STATUS", "active", "s1"))
    kb.supersede("k1", KnowledgeItem("k2", "A", "STATUS", "closed", "s2", 2))
    assert kb.items["k1"].status == "superseded"
    assert kb.trusted("k2").object == "closed"
