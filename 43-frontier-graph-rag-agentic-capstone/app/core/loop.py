"""A bounded, deterministic control loop for AegisAI."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Generic, TypeVar


class RunState(str, Enum):
    OBSERVE = "observe"
    DECIDE = "decide"
    ACT = "act"
    VERIFY = "verify"
    WAIT = "wait"
    RECOVER = "recover"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class RunContext:
    task_id: str
    max_steps: int = 20
    step: int = 0
    state: RunState = RunState.OBSERVE
    progress: list[str] = field(default_factory=list)
    events: list[dict] = field(default_factory=list)

    def emit(self, event: str, **data) -> None:
        self.events.append({"step": self.step, "event": event, **data})


T = TypeVar("T")


class BoundedAgentLoop(Generic[T]):
    """Run an observe/decide/act/verify cycle with explicit termination."""

    def __init__(
        self,
        observe: Callable[[RunContext], T],
        decide: Callable[[RunContext, T], object | None],
        act: Callable[[RunContext, object], object],
        verify: Callable[[RunContext, object], bool],
    ) -> None:
        self.observe = observe
        self.decide = decide
        self.act = act
        self.verify = verify

    def run(self, context: RunContext) -> RunContext:
        while context.step < context.max_steps:
            context.step += 1
            try:
                context.state = RunState.OBSERVE
                observation = self.observe(context)
                context.emit("observed")

                context.state = RunState.DECIDE
                action = self.decide(context, observation)
                if action is None:
                    context.state = RunState.COMPLETED
                    context.emit("stopped_no_action")
                    return context

                context.state = RunState.ACT
                result = self.act(context, action)
                context.emit("acted")

                context.state = RunState.VERIFY
                if self.verify(context, result):
                    context.state = RunState.COMPLETED
                    context.emit("verified")
                    return context

                context.state = RunState.RECOVER
                context.progress.append("verification_failed")
                context.emit("verification_failed")
            except Exception as exc:  # boundary: convert execution failure to run evidence
                context.state = RunState.RECOVER
                context.emit("error", error_type=type(exc).__name__)
                context.progress.append("execution_error")

        context.state = RunState.FAILED
        context.emit("budget_exhausted")
        return context
