import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from graph.core import Claim, Edge, Entity, GraphValidationError, KnowledgeGraph


def graph():
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "company", "A", "t1", ("s1",)))
    g.add_entity(Entity("b", "company", "B", "t1", ("s2",)))
    g.add_entity(Entity("x", "company", "X", "t2", ("s3",)))
    return g


def test_edge_requires_provenance():
    g = graph()
    with pytest.raises(GraphValidationError):
        g.add_edge(Edge("a", "OWNS", "b", "missing", "t1"))


def test_cross_tenant_edge_is_denied():
    g = graph()
    g.add_claim(Claim("c1", "a", "OWNS", "b", "A owns B", "s1", "t1"))
    with pytest.raises(GraphValidationError):
        g.add_edge(Edge("a", "OWNS", "x", "c1", "t1"))


def test_bounded_neighbors_are_deterministic():
    g = graph()
    g.add_claim(Claim("c1", "a", "OWNS", "b", "A owns B", "s1", "t1"))
    g.add_edge(Edge("a", "OWNS", "b", "c1", "t1"))
    assert [e.entity_id for e in g.neighbors("a", "t1", 1)] == ["b"]
    assert g.neighbors("a", "t2", 1) == []


def test_unbounded_traversal_is_rejected():
    g = graph()
    with pytest.raises(GraphValidationError):
        g.neighbors("a", "t1", 6)
