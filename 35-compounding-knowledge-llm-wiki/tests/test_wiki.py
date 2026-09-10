from app.wiki import Claim, Evidence, Wiki


def test_evidence_backed_update_supersedes_history():
    w = Wiki()
    w.register_evidence(Evidence.from_text("e1", "policy-v1", "retention is 90 days", tenant="acme"))
    w.register_evidence(Evidence.from_text("e2", "policy-v2", "retention is 30 days", tenant="acme"))
    first = w.upsert(Claim("retention", "retention is 90 days", "policy-v1", evidence_id="e1", tenant="acme"))
    second = w.upsert(Claim("retention", "retention is 30 days", "policy-v2", evidence_id="e2", tenant="acme"))
    assert second.version == 2
    assert w.active("retention", "acme").text == "retention is 30 days"
    assert any(c.identity() == first.identity() and c.status == "SUPERSEDED" for c in w.claims["retention"])


def test_unknown_evidence_is_rejected():
    w = Wiki()
    try:
        w.upsert(Claim("topic", "claim", "source", evidence_id="missing"))
    except ValueError as exc:
        assert "unknown evidence" in str(exc)
    else:
        raise AssertionError("claim without registered evidence must fail")


def test_cross_tenant_reference_is_denied():
    w = Wiki()
    w.register_evidence(Evidence.from_text("e1", "src", "secret", tenant="tenant-a"))
    try:
        w.upsert(Claim("topic", "claim", "src", evidence_id="e1", tenant="tenant-b"))
    except PermissionError:
        pass
    else:
        raise AssertionError("cross-tenant evidence must be denied")


def test_context_is_bounded_and_provenance_is_measurable():
    w = Wiki()
    w.register_evidence(Evidence.from_text("e1", "src", "A" * 100, tenant="a"))
    w.upsert(Claim("a", "A" * 100, "src", evidence_id="e1", tenant="a"))
    context = w.compile_context(["a"], tenant="a", max_chars=40)
    assert len(context) <= 40
    assert w.provenance_coverage("a") == 1.0


def test_rollback_restores_previous_version_without_erasing_history():
    w = Wiki()
    w.register_evidence(Evidence.from_text("e1", "v1", "alpha"))
    w.register_evidence(Evidence.from_text("e2", "v2", "beta"))
    w.upsert(Claim("x", "alpha", "v1", evidence_id="e1"))
    w.upsert(Claim("x", "beta", "v2", evidence_id="e2"))
    restored = w.rollback("x", 1)
    assert restored.text == "alpha"
    assert w.active("x").text == "alpha"
    assert any(c.text == "beta" and c.status == "ROLLED_BACK" for c in w.claims["x"])


def test_quarantine_is_audited():
    w = Wiki()
    claim = Claim("x", "suspicious", "unknown")
    w.quarantine(claim, "poisoning signal")
    assert w.quarantined == [claim]
    assert w.changes[-1].action == "QUARANTINE"
