from datetime import datetime, timedelta, timezone
from app.memory import Memory, MemoryStore, ttl_memory

def test_tenant_isolation():
    s=MemoryStore(); s.put(Memory('1','A','semantic','python is used','doc'))
    assert s.search('python','B') == []

def test_retrieval_ranking():
    s=MemoryStore(); s.put(Memory('1','A','semantic','python async client','x',.9,.9)); s.put(Memory('2','A','semantic','database schema','y',1,.2))
    assert s.search('python client','A')[0].memory_id == '1'

def test_expiry_and_delete():
    s=MemoryStore(); m=ttl_memory('1','A','episodic','temporary fact','x',1); s.put(m)
    assert s.get('1','A') is not None
    expired=Memory('2','A','episodic','old','x',expires_at=datetime.now(timezone.utc)-timedelta(seconds=1)); s.put(expired)
    assert s.get('2','A') is None
    s.delete('1'); assert s.get('1','A') is None

def test_contradiction_signal():
    s=MemoryStore(); old=Memory('1','A','semantic','region is east','doc1'); new=Memory('2','A','semantic','region is west','doc2')
    s.put(old)
    assert s.contradicts(new,[old]) == [old]
