from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import hashlib
from typing import Any, Callable

class DecisionType(str, Enum):
    FINAL='final'; TOOL='tool'; REFLECT='reflect'; WAIT='wait'; ABORT='abort'

@dataclass(frozen=True)
class Decision:
    kind: DecisionType
    tool: str | None = None
    args: dict[str, Any] = field(default_factory=dict)
    reason: str = ''

@dataclass
class AgentState:
    goal: str
    observations: list[Any] = field(default_factory=list)
    actions: list[Decision] = field(default_factory=list)
    tool_results: list[Any] = field(default_factory=list)
    steps: int = 0
    reflections: int = 0
    done: bool = False
    termination_reason: str | None = None

class AgentLoop:
    def __init__(self, decide: Callable[[AgentState], Decision], tools: dict[str, Callable[..., Any]], max_steps: int = 10, max_reflections: int = 2):
        self.decide, self.tools = decide, tools
        self.max_steps, self.max_reflections = max_steps, max_reflections

    @staticmethod
    def fingerprint(state: AgentState) -> str:
        raw = repr((state.goal, state.observations[-3:], [(a.kind.value, a.tool, sorted(a.args.items())) for a in state.actions[-3:]]))
        return hashlib.sha256(raw.encode()).hexdigest()

    def run(self, state: AgentState) -> AgentState:
        seen: set[str] = set()
        while not state.done:
            if state.steps >= self.max_steps:
                state.termination_reason = 'step_budget'; break
            fp = self.fingerprint(state)
            if fp in seen:
                state.termination_reason = 'repeated_state'; break
            seen.add(fp)
            decision = self.decide(state)
            state.actions.append(decision)
            state.steps += 1
            if decision.kind is DecisionType.FINAL:
                state.done = True; state.termination_reason = 'verified_final'; break
            if decision.kind is DecisionType.ABORT:
                state.done = True; state.termination_reason = 'agent_abort'; break
            if decision.kind is DecisionType.WAIT:
                state.termination_reason = 'waiting'; break
            if decision.kind is DecisionType.REFLECT:
                state.reflections += 1
                if state.reflections > self.max_reflections:
                    state.termination_reason = 'reflection_budget'; break
                state.observations.append({'reflection': decision.reason})
                continue
            if decision.kind is DecisionType.TOOL:
                if not decision.tool or decision.tool not in self.tools:
                    state.termination_reason = 'invalid_tool'; break
                try:
                    result = self.tools[decision.tool](**decision.args)
                    state.tool_results.append(result)
                    state.observations.append({'tool': decision.tool, 'result': result})
                except Exception as exc:
                    state.observations.append({'tool_error': type(exc).__name__, 'message': str(exc)})
        return state
