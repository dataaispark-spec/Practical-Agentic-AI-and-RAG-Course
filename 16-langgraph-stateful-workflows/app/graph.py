from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class Status(str, Enum): RUNNING='running'; WAITING='waiting'; COMPLETED='completed'; FAILED='failed'

@dataclass
class GraphState:
    data: dict[str, Any] = field(default_factory=dict)
    status: Status = Status.RUNNING
    current: str = 'start'
    history: list[str] = field(default_factory=list)
    retries: dict[str, int] = field(default_factory=dict)
    error: str | None = None

@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    condition: Callable[[GraphState], bool] | None = None

class StateGraph:
    def __init__(self, max_transitions: int = 50):
        self.nodes: dict[str, Callable[[GraphState], None]] = {}
        self.edges: list[Edge] = []
        self.max_transitions = max_transitions

    def add_node(self, name: str, fn: Callable[[GraphState], None]) -> None:
        self.nodes[name] = fn

    def add_edge(self, source: str, target: str, condition=None) -> None:
        self.edges.append(Edge(source, target, condition))

    def next_node(self, state: GraphState) -> str | None:
        for e in self.edges:
            if e.source == state.current and (e.condition is None or e.condition(state)):
                return e.target
        return None

    def run(self, state: GraphState, start: str = 'start') -> GraphState:
        state.current = start
        for _ in range(self.max_transitions):
            if state.current == 'END':
                state.status = Status.COMPLETED; return state
            fn = self.nodes.get(state.current)
            if fn is None:
                state.status = Status.FAILED; state.error = f'unknown node: {state.current}'; return state
            state.history.append(state.current)
            try:
                fn(state)
            except Exception as exc:
                state.status = Status.FAILED; state.error = f'{type(exc).__name__}: {exc}'; return state
            if state.status is Status.WAITING:
                return state
            nxt = self.next_node(state)
            if nxt is None:
                state.status = Status.COMPLETED; return state
            state.current = nxt
        state.status = Status.FAILED; state.error = 'transition budget exceeded'; return state
