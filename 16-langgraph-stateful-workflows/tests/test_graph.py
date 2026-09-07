from app.graph import GraphState, StateGraph, Status

def test_conditional_routing():
    g=StateGraph(); g.add_node('start',lambda s:s.data.update(ok=True)); g.add_node('yes',lambda s:s.data.update(result='approved')); g.add_edge('start','yes',lambda s:s.data['ok']); g.add_edge('yes','END')
    s=g.run(GraphState(), 'start'); assert s.status is Status.COMPLETED; assert s.data['result']=='approved'

def test_waiting_interrupt():
    g=StateGraph(); g.add_node('start',lambda s:setattr(s,'status',Status.WAITING)); g.add_edge('start','END')
    s=g.run(GraphState(),'start'); assert s.status is Status.WAITING

def test_cycle_budget():
    g=StateGraph(max_transitions=3); g.add_node('a',lambda s:None); g.add_node('b',lambda s:None); g.add_edge('a','b'); g.add_edge('b','a')
    s=g.run(GraphState(),'a'); assert s.status is Status.FAILED; assert 'budget' in s.error
