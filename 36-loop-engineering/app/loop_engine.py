from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class Phase(str, Enum):
    OBSERVE='observe'; DECIDE='decide'; ACT='act'; VERIFY='verify'; RECOVER='recover'; STOP='stop'

@dataclass
class LoopState:
    goal: str
    phase: Phase = Phase.OBSERVE
    steps: int = 0
    tool_calls: int = 0
    observations: list[Any] = field(default_factory=list)
    actions: list[dict[str, Any]] = field(default_factory=list)
    verified: bool = False
    reason: str | None = None

class LoopBudgetExceeded(RuntimeError): pass

class ProductionLoop:
    def __init__(self, decide: Callable[[LoopState], dict[str, Any]], tools: dict[str, Callable[..., Any]], verify: Callable[[LoopState], bool], max_steps=8, max_tool_calls=8):
        self.decide, self.tools, self.verify = decide, tools, verify
        self.max_steps, self.max_tool_calls = max_steps, max_tool_calls

    def run(self, state: LoopState) -> LoopState:
        seen = set()
        while state.phase is not Phase.STOP:
            if state.steps >= self.max_steps: state.reason='step_budget'; state.phase=Phase.STOP; break
            fingerprint = repr((state.phase.value, state.goal, state.observations[-2:], state.actions[-2:]))
            if fingerprint in seen: state.reason='no_progress'; state.phase=Phase.STOP; break
            seen.add(fingerprint); state.steps += 1
            if state.phase is Phase.OBSERVE: state.phase=Phase.DECIDE
            elif state.phase is Phase.DECIDE:
                decision=self.decide(state); state.actions.append(decision); state.phase=Phase.ACT
            elif state.phase is Phase.ACT:
                action=state.actions[-1]
                if action.get('type')=='final': state.phase=Phase.VERIFY; continue
                tool=action.get('tool')
                if tool not in self.tools: state.reason='invalid_tool'; state.phase=Phase.STOP; break
                if state.tool_calls >= self.max_tool_calls: state.reason='tool_budget'; state.phase=Phase.STOP; break
                state.tool_calls += 1
                try: state.observations.append(self.tools[tool](**action.get('args', {}))); state.phase=Phase.VERIFY
                except Exception as exc: state.observations.append({'error':type(exc).__name__}); state.phase=Phase.RECOVER
            elif state.phase is Phase.VERIFY:
                if self.verify(state): state.verified=True; state.reason='verified'; state.phase=Phase.STOP
                else: state.phase=Phase.RECOVER
            elif state.phase is Phase.RECOVER:
                if state.tool_calls >= self.max_tool_calls: state.reason='recovery_budget'; state.phase=Phase.STOP
                else: state.phase=Phase.OBSERVE
        return state
