from app.pipeline import RawDocument, detect_pii, parse, protect, redact, validate


def test_parse_preserves_page_boundaries_and_version_lineage():
    doc = RawDocument("d1", "t1", "s3://docs/a", "one\n\ntwo\fthree", acl=("analyst",), source_version="v7", pipeline_version="p3")
    elements = parse(doc)
    assert [e.page for e in elements] == [1, 1, 2]
    assert len({e.element_id for e in elements}) == 3


def test_detect_pii_finds_email():
    findings = detect_pii("Contact alice@example.com for help")
    assert any(f.kind == "email" and f.confidence > 0.9 for f in findings)


def test_redaction_is_deterministic():
    findings = detect_pii("alice@example.com")
    assert redact("alice@example.com", findings) == "[EMAIL_REDACTED]"


def test_protection_preserves_security_and_lineage_metadata():
    raw = RawDocument("d1", "tenant-a", "s3://docs/a", "mail alice@example.com", acl=("legal",), source_version="v2", pipeline_version="p9")
    protected = protect(raw)
    assert protected.tenant_id == "tenant-a"
    assert protected.acl == ("legal",)
    assert protected.source_version == "v2"
    assert protected.pipeline_version == "p9"
    assert protected.source_content_hash != protected.content_hash
    assert "alice@example.com" not in protected.text


def test_missing_acl_fails_closed():
    raw = RawDocument("d1", "tenant-a", "s3://docs/a", "safe text")
    protected = protect(raw, allowed_kinds={"email"})
    assert "missing ACL" in validate(protected)


def test_card_like_low_confidence_is_quarantined():
    raw = RawDocument("d1", "tenant-a", "s3://docs/a", "reference 4111 1111 1111 1111", acl=("security",))
    protected = protect(raw)
    assert protected.quarantined is True
    assert any(f.kind == "card_like" for f in protected.findings)
