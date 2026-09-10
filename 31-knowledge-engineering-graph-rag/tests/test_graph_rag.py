from app.graph import Edge, Entity, KnowledgeGraph
from app.retrieval import shortest_paths


def test_provenance_and_tenant_boundary():
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "supplier", "A", "t1"))
    g.add_entity(Entity("b", "system", "B", "t1"))
    g.add_edge(Edge("a", "OWNS", "b", "src-1", "t1"))
    assert shortest_paths(g, "a", "b", "t1", 1)


def test_cross_tenant_edge_is_rejected():
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "supplier", "A", "t1"))
    g.add_entity(Entity("b", "system", "B", "t2"))
    try:
        g.add_edge(Edge("a", "OWNS", "b", "src", "t1"))
    except PermissionError:
        return
    raise AssertionError("cross-tenant edge was accepted")
