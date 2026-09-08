from dataclasses import dataclass, field
from typing import Any

@dataclass
class Task:
    goal: str
    tenant: str
    risk: str = "low"
    allowed_tools: set[str] = field(default_factory=set)
    budget: float = 1.0
    verified: bool = False

@dataclass
class Evidence:
    source_id: str
    claim: str
    authorized: bool = True

class AegisAI:
    """Framework-free educational capstone kernel."""
    def __init__(self):
        self.events: list[dict[str, Any]] = []

    def authorize(self, task: Task, tool: str) -> bool:
        ok = tool in task.allowed_tools
        self.events.append({"kind": "policy", "tool": tool, "allowed": ok})
        return ok

    def verify(self, task: Task, evidence: list[Evidence]) -> bool:
        task.verified = bool(evidence) and all(e.authorized for e in evidence)
        self.events.append({"kind": "verify", "verified": task.verified})
        return task.verified
