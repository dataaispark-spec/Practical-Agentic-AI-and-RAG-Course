from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from typing import Iterable


@dataclass(frozen=True)
class DocumentElement:
    element_id: str
    page: int
    section: str
    element_type: str
    text: str


@dataclass(frozen=True)
class RawDocument:
    document_id: str
    tenant_id: str
    source_uri: str
    text: str
    sensitivity: str = "internal"
    acl: tuple[str, ...] = ()
    source_version: str = "1"
    pipeline_version: str = "1"


@dataclass(frozen=True)
class Finding:
    kind: str
    start: int
    end: int
    value: str
    confidence: float


@dataclass(frozen=True)
class ProtectedDocument:
    document_id: str
    tenant_id: str
    source_uri: str
    text: str
    findings: tuple[Finding, ...]
    content_hash: str
    source_content_hash: str
    source_version: str
    pipeline_version: str
    quarantined: bool
    reason: str | None = None
    sensitivity: str = "internal"
    acl: tuple[str, ...] = ()


EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"(?<!\d)(?:\+?\d[\d ()-]{7,}\d)(?!\d)")
CARD = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")


def parse(raw: RawDocument) -> tuple[DocumentElement, ...]:
    """Minimal deterministic parser preserving page and element lineage."""
    elements: list[DocumentElement] = []
    for page, page_text in enumerate(raw.text.split("\f"), start=1):
        for number, block in enumerate(page_text.split("\n\n"), start=1):
            text = block.strip()
            if not text:
                continue
            digest = hashlib.sha256(f"{raw.document_id}:{raw.source_version}:{page}:{number}:{text}".encode()).hexdigest()[:16]
            elements.append(DocumentElement(digest, page, "default", "paragraph", text))
    return tuple(elements)


def detect_pii(text: str) -> tuple[Finding, ...]:
    findings: list[Finding] = []
    for kind, pattern, confidence in (
        ("email", EMAIL, 0.99),
        ("phone", PHONE, 0.85),
        ("card_like", CARD, 0.70),
    ):
        for match in pattern.finditer(text):
            findings.append(Finding(kind, match.start(), match.end(), match.group(), confidence))
    # Remove overlapping lower-priority matches deterministically.
    selected: list[Finding] = []
    for finding in sorted(findings, key=lambda f: (f.start, -(f.end - f.start), -f.confidence)):
        if any(finding.start < existing.end and existing.start < finding.end for existing in selected):
            continue
        selected.append(finding)
    return tuple(sorted(selected, key=lambda f: (f.start, f.end)))


def redact(text: str, findings: Iterable[Finding]) -> str:
    result = text
    for finding in sorted(findings, key=lambda f: f.start, reverse=True):
        result = result[: finding.start] + f"[{finding.kind.upper()}_REDACTED]" + result[finding.end :]
    return result


def protect(raw: RawDocument, allowed_kinds: set[str] | None = None) -> ProtectedDocument:
    findings = detect_pii(raw.text)
    allowed = allowed_kinds or set()
    prohibited = tuple(f for f in findings if f.kind not in allowed)
    protected_text = redact(raw.text, prohibited)
    # Low-confidence prohibited findings require human review rather than silent indexing.
    quarantined = any(f.confidence < 0.75 for f in prohibited)
    reason = "low-confidence sensitive finding requires review" if quarantined else None
    source_hash = hashlib.sha256(raw.text.encode("utf-8")).hexdigest()
    protected_hash = hashlib.sha256(protected_text.encode("utf-8")).hexdigest()
    return ProtectedDocument(
        raw.document_id,
        raw.tenant_id,
        raw.source_uri,
        protected_text,
        findings,
        protected_hash,
        source_hash,
        raw.source_version,
        raw.pipeline_version,
        quarantined,
        reason,
        raw.sensitivity,
        raw.acl,
    )


def validate(document: ProtectedDocument) -> list[str]:
    errors: list[str] = []
    if not document.document_id:
        errors.append("missing document_id")
    if not document.tenant_id:
        errors.append("missing tenant_id")
    if not document.source_uri:
        errors.append("missing source_uri")
    if not document.acl:
        errors.append("missing ACL")
    if not document.source_version:
        errors.append("missing source_version")
    if not document.pipeline_version:
        errors.append("missing pipeline_version")
    if document.quarantined:
        errors.append(document.reason or "quarantined")
    if not document.content_hash or not document.source_content_hash:
        errors.append("missing content_hash")
    return errors
