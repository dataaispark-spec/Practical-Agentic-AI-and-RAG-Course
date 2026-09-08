import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "00-course-toolkit"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from graph.core import Claim, Edge, Entity, KnowledgeGraph
from app.graph_observation import build_graph_observation


def test_graph_observation_is_tenant_scoped_and_bounded():
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "company", "A", "t1"))
    g.add_entity(Entity("b", "company", "B", "t1"))
    g.add_entity(Entity("x", "company", "X", "t2"))
    g.add_claim(Claim("c1", "a", "OWNS", "b", "A owns B", "s1", "t1"))
    g.add_edge(Edge("a", "OWNS", "b", "c1", "t1"))
    obs = build_graph_observation(g, "a", "t1", 1)
    assert [e["entity_id"] for e in obs.entities] == ["b"]
    assert obs.evidence_claim_ids == ("c1",)
    assert build_graph_observation(g, "a", "t2", 1).entities == ()
