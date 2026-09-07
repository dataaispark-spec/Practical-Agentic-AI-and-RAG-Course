from app.release import Gate, GateStatus, ReleaseManifest, release_status, validate_manifest


def manifest():
    return ReleaseManifest('aegis','1.0','sha256:abc','m1','p1','r1','pol1','eval1')


def test_manifest_complete():
    assert validate_manifest(manifest()) == []


def test_manifest_detects_missing_fields():
    m=ReleaseManifest('aegis','','sha256:abc','m1','p1','r1','pol1','eval1')
    assert 'application_version' in validate_manifest(m)


def test_block_wins():
    assert release_status([Gate('security',GateStatus.PASS),Gate('eval',GateStatus.BLOCK)]) is GateStatus.BLOCK


def test_warn_when_no_block():
    assert release_status([Gate('security',GateStatus.PASS),Gate('eval',GateStatus.WARN)]) is GateStatus.WARN


def test_pass():
    assert release_status([Gate('security',GateStatus.PASS)]) is GateStatus.PASS
