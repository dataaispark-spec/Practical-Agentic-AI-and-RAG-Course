from app.server import Capability, EnterpriseServer, Principal, Request, ServerError, canonical_hash


def make_server():
    return EnterpriseServer(
        [Capability("read_customer", "tool", roles=frozenset({"reader","admin"})), Capability("update_customer", "tool", risk="high", roles=frozenset({"admin"}))],
        {"read_customer": lambda customer_id: {"id": customer_id}, "update_customer": lambda customer_id, status: {"id": customer_id, "status": status}},
    )


def test_discovery():
    assert {c.name for c in make_server().discover()} == {"read_customer","update_customer"}


def test_tenant_and_role_authorization():
    s=make_server(); p=Principal("u1","t1",frozenset({"reader"}))
    assert s.execute(p,Request("1","read_customer",{"customer_id":"c1"},"t1"))["id"]=="c1"
    try: s.execute(p,Request("2","update_customer",{"customer_id":"c1","status":"x"},"t1","k1"))
    except ServerError as e: assert "role" in str(e)
    else: raise AssertionError("expected role denial")


def test_tenant_isolation():
    s=make_server(); p=Principal("u1","t1",frozenset({"reader"}))
    try: s.execute(p,Request("1","read_customer",{"customer_id":"c1"},"t2"))
    except ServerError as e: assert "tenant" in str(e)
    else: raise AssertionError("expected tenant denial")


def test_high_risk_requires_idempotency():
    s=make_server(); p=Principal("u1","t1",frozenset({"admin"}))
    try: s.execute(p,Request("1","update_customer",{"customer_id":"c1","status":"x"},"t1"))
    except ServerError as e: assert "idempotency" in str(e)
    else: raise AssertionError("expected idempotency requirement")


def test_idempotent_mutation():
    s=make_server(); p=Principal("u1","t1",frozenset({"admin"})); r=Request("1","update_customer",{"customer_id":"c1","status":"x"},"t1","same")
    assert s.execute(p,r)==s.execute(p,r)
    assert len(s.audit)==1


def test_canonical_hash_is_stable():
    a=Request("1","x",{"b":2,"a":1},"t1"); b=Request("2","x",{"a":1,"b":2},"t1")
    assert canonical_hash(a)==canonical_hash(b)
