import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import AegisAI, Evidence, Task


def test_authorization_is_explicit():
    a = AegisAI()
    task = Task("investigate", "tenant-a", allowed_tools={"search"})
    assert a.authorize(task, "search") is True
    assert a.authorize(task, "refund") is False


def test_verification_requires_authorized_evidence():
    a = AegisAI()
    task = Task("investigate", "tenant-a")
    assert a.verify(task, [Evidence("doc-1", "supported")]) is True
    task2 = Task("investigate", "tenant-a")
    assert a.verify(task2, [Evidence("doc-2", "bad", authorized=False)]) is False
