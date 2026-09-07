from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FailureClass(str, Enum):
    RETRIEVAL = "retrieval"
    MODEL = "model"
    TOOL = "tool"
    POLICY = "policy"
    STATE = "state"
    COORDINATION = "coordination"
    SECURITY = "security"
    BUDGET = "budget"
    EXTERNAL = "external_dependency"
    CONTRACT = "contract"


@dataclass(frozen=True)
class TraceEvent:
    event_id: str
    run_id: str
    parent_id: str | None
    causation_id: str | None
    event_type: str
    component: str
    timestamp: float
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Failure:
    event_id: str
    failure_class: FailureClass
    reason: str
    severity: str = "error"


class TraceDebugger:
    def __init__(self, events: list[TraceEvent]):
        self.events = sorted(events, key=lambda e: e.timestamp)

    def by_run(self, run_id: str) -> list[TraceEvent]:
        return [e for e in self.events if e.run_id == run_id]

    def causal_chain(self, event_id: str) -> list[TraceEvent]:
        by_id = {e.event_id: e for e in self.events}
        chain: list[TraceEvent] = []
        current = by_id.get(event_id)
        while current:
            chain.append(current)
            current = by_id.get(current.causation_id) if current.causation_id else None
        return list(reversed(chain))

    def first_failure(self, failures: list[Failure]) -> Failure | None:
        if not failures:
            return None
        order = {e.event_id: i for i, e in enumerate(self.events)}
        return min(failures, key=lambda f: order.get(f.event_id, 10**9))

    def trace_diff(self, other: "TraceDebugger") -> list[tuple[str, str, str]]:
        left = [(e.event_type, e.component) for e in self.events]
        right = [(e.event_type, e.component) for e in other.events]
        diffs = []
        for i in range(max(len(left), len(right))):
            a = left[i] if i < len(left) else ("<missing>", "<missing>")
            b = right[i] if i < len(right) else ("<missing>", "<missing>")
            if a != b:
                diffs.append((str(i), str(a), str(b)))
        return diffs

    def latency_by_component(self) -> dict[str, float]:
        grouped: dict[str, list[float]] = {}
        for a, b in zip(self.events, self.events[1:]):
            grouped.setdefault(a.component, []).append(max(0.0, b.timestamp - a.timestamp))
        return {component: sum(values) for component, values in grouped.items()}

    def cost_by_component(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for event in self.events:
            cost = float(event.attributes.get("cost_usd", 0.0))
            result[event.component] = result.get(event.component, 0.0) + cost
        return result

    def security_events(self) -> list[TraceEvent]:
        return [e for e in self.events if e.event_type.startswith("security.") or e.attributes.get("security")]


def validate_trace(events: list[TraceEvent]) -> list[str]:
    errors: list[str] = []
    ids = {e.event_id for e in events}
    for e in events:
        if e.causation_id and e.causation_id not in ids:
            errors.append(f"{e.event_id}: missing causation event")
        if not e.run_id:
            errors.append(f"{e.event_id}: missing run_id")
        if e.timestamp < 0:
            errors.append(f"{e.event_id}: invalid timestamp")
    return errors
