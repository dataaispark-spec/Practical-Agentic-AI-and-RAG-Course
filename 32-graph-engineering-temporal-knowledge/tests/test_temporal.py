from datetime import date
from app.temporal import TemporalEdge, detect_overlap

def test_active_on():
    e=TemporalEdge('a','OWNS','b',date(2025,1,1),date(2025,6,30),'s')
    assert e.active_on(date(2025,3,1)); assert not e.active_on(date(2025,7,1))

def test_overlap():
    a=TemporalEdge('a','OWNS','b',date(2025,1,1),date(2025,6,30),'s1')
    b=TemporalEdge('a','OWNS','b',date(2025,6,1),None,'s2')
    assert detect_overlap([a,b])
