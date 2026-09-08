import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "00-course-toolkit"))

from app.graph_rag import bounded_graph_retrieve, reciprocal_rank_fusion
from graph.core import Claim, Edge, Entity, KnowledgeGraph


def test_graph_rag_is_bounded_and_tenant_safe():
    g = KnowledgeGraph()
    for eid, tenant in (("a", "t1"), ("b", "t1"), ("c", "t1"), ("x", "t2")):
        g.add_entity(Entity(eid, "node", eid.upper(), tenant))
    g.add_claim(Claim("c1", "a", "LINKS", "b", "a-b", "s1", "t1"))
    g.add_claim(Claim("c2", "b", "LINKS", "c", "b-c", "s2", "t1"))
    g.add_edge(Edge("a", "LINKS", "b", "c1", "t1"))
    g.add_edge(Edge("b", "LINKS", "c", "c2", "t1"))
    assert [h.entity_id for h in bounded_graph_retrieve(g, "a", "t1", 1)] == ["b"]
    assert [h.entity_id for h in bounded_graph_retrieve(g, "a", "t1", 2)] == ["b", "c"]
    assert bounded_graph_retrieve(g, "a", "t2") == []


def test_hybrid_fusion_is_deterministic():
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "node", "A", "t1"))
    g.add_entity(Entity("b", "node", "B", "t1"))
    g.add_claim(Claim("c1", "a", "LINKS", "b", "a-b", "s1", "t1"))
    g.add_edge(Edge("a", "LINKS", "b", "c1", "t1"))
    hits = bounded_graph_retrieve(g, "a", "t1")
    assert reciprocal_rank_fusion(hits, ["b"]) == ["b"]
