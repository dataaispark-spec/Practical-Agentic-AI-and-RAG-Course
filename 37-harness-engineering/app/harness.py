from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass
class HarnessState:
    task: str
    context: list[Any] = field(default_factory=list)
    tool_calls: int = 0
    approved: bool = False
    events: list[dict[str, Any]] = field(default_factory=list)

class Harness:
    def __init__(self, model: Callable[[str, list[Any]], dict[str, Any]], tools: dict[str, Callable[..., Any]], policy: Callable[[dict[str, Any]], bool], max_tool_calls=8):
        self.model, self.tools, self.policy, self.max_tool_calls = model, tools, policy, max_tool_calls

    def step(self, state: HarnessState) -> HarnessState:
        decision=self.model(state.task, state.context)
        state.events.append({'kind':'decision','decision':decision})
        if decision.get('type')=='final': return state
        tool=decision.get('tool')
        if tool not in self.tools or state.tool_calls >= self.max_tool_calls: raise RuntimeError('tool boundary violation')
        if not self.policy(decision): raise PermissionError('policy denied action')
        state.tool_calls += 1
        result=self.tools[tool](**decision.get('args', {}))
        state.context.append({'tool':tool,'result':result})
        state.events.append({'kind':'tool_result','tool':tool})
        return state
