from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from statistics import quantiles
from typing import Any


class Signal(str, Enum):
    TRACE = "trace"
    METRIC = "metric"
    EVENT = "event"


@dataclass(frozen=True)
class Span:
    span_id: str
    trace_id: str
    parent_id: str | None
    tenant_id: str
    component: str
    operation: str
    started_at: float
    ended_at: float
    attributes: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        return max(0.0, self.ended_at - self.started_at) * 1000


@dataclass(frozen=True)
class Metric:
    name: str
    value: float
    tenant_id: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Event:
    event_id: str
    trace_id: str
    tenant_id: str
    event_type: str
    timestamp: float
    attributes: dict[str, Any] = field(default_factory=dict)


class TelemetryStore:
    def __init__(self):
        self.spans: list[Span] = []
        self.metrics: list[Metric] = []
        self.events: list[Event] = []

    def add_span(self, span: Span) -> None:
        if not span.trace_id or not span.tenant_id:
            raise ValueError("trace and tenant are required")
        self.spans.append(span)

    def add_metric(self, metric: Metric) -> None:
        self.metrics.append(metric)

    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def trace(self, trace_id: str, tenant_id: str) -> list[Span]:
        return sorted((s for s in self.spans if s.trace_id == trace_id and s.tenant_id == tenant_id), key=lambda s: s.started_at)

    def events_for(self, trace_id: str, tenant_id: str) -> list[Event]:
        return sorted((e for e in self.events if e.trace_id == trace_id and e.tenant_id == tenant_id), key=lambda e: e.timestamp)

    def cost(self, trace_id: str, tenant_id: str) -> float:
        return sum(float(s.attributes.get("cost_usd", 0.0)) for s in self.trace(trace_id, tenant_id))

    def token_count(self, trace_id: str, tenant_id: str) -> int:
        return sum(int(s.attributes.get("tokens", 0)) for s in self.trace(trace_id, tenant_id))


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    qs = quantiles(values, n=100, method="inclusive")
    return qs[max(0, min(98, int(p) - 1))]


def critical_path(spans: list[Span]) -> float:
    """Educational approximation: longest parent/child chain by span duration."""
    by_parent: dict[str | None, list[Span]] = {}
    for s in spans:
        by_parent.setdefault(s.parent_id, []).append(s)

    def depth(span: Span) -> float:
        children = by_parent.get(span.span_id, [])
        return span.duration_ms + max((depth(c) for c in children), default=0.0)

    roots = by_parent.get(None, [])
    return max((depth(s) for s in roots), default=0.0)


def detect_retry_amplification(spans: list[Span], threshold: int = 3) -> list[str]:
    counts: dict[tuple[str, str], int] = {}
    for s in spans:
        key = (s.component, s.operation)
        counts[key] = counts.get(key, 0) + int(s.attributes.get("attempt", 1) > 1)
    return [f"{component}:{operation}" for (component, operation), n in counts.items() if n >= threshold]
