from app.graph import Entity, Edge, KnowledgeGraph

def graph():
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "company", "A", "t1"))
    g.add_entity(Entity("b", "company", "B", "t1"))
    g.add_entity(Entity("c", "person", "C", "t1"))
    g.add_edge(Edge("a", "OWNS", "b", "t1", "src-1"))
    g.add_edge(Edge("b", "HAS_CEO", "c", "t1", "src-2"))
    return g

def test_bounded_multihop():
    assert graph().neighbors("a", "t1", 2) == {"a", "b", "c"}

def test_provenance_required():
    g = graph()
    try:
        g.add_edge(Edge("a", "OWNS", "b", "t1", ""))
    except ValueError:
        return
    assert False

def test_tenant_boundary():
    g = graph(); g.add_entity(Entity("x", "company", "X", "t2"))
    try:
        g.add_edge(Edge("a", "OWNS", "x", "t1", "src"))
    except PermissionError:
        return
    assert False
