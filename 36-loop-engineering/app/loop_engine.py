"""Mechanism-first reference implementation for Module 36 — Loop Engineering."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class Phase(str, Enum):
    START = "START"
    OBSERVE = "OBSERVE"
    DECIDE = "DECIDE"
    POLICY = "POLICY"
    ACT = "ACT"
    VERIFY = "VERIFY"
    RECOVER = "RECOVER"
    COMPLETE = "COMPLETE"
    STOP = "STOP"
    ESCALATE = "ESCALATE"


class Outcome(str, Enum):
    PASS = "PASS"
    RETRY = "RETRY"
    RECOVER = "RECOVER"
    REPLAN = "REPLAN"
    ESCALATE = "ESCALATE"
    STOP = "STOP"


@dataclass(frozen=True)
class Task:
    task_id: str
    tenant_id: str
    objective: str
    max_steps: int = 12
    max_tool_calls: int = 20
    max_model_calls: int = 20
    max_cost: float = 1.0
    max_repeated_states: int = 2


@dataclass(frozen=True)
class Observation:
    observation_id: str
    source: str
    payload: Dict[str, Any]
    state_version: int
    fresh: bool = True


@dataclass(frozen=True)
class Proposal:
    action: str
    arguments: Dict[str, Any]
    expected: str = ""
    reason: str = ""


@dataclass
class TraceEvent:
    phase: Phase
    detail: Dict[str, Any]


@dataclass
class LoopState:
    task: Task
    phase: Phase = Phase.START
    step: int = 0
    state_version: int = 0
    observation: Optional[Observation] = None
    proposal: Optional[Proposal] = None
    last_action_id: Optional[str] = None
    completed_action_ids: Set[str] = field(default_factory=set)
    verified: bool = False
    result: Optional[str] = None
    stop_reason: Optional[str] = None
    model_calls: int = 0
    tool_calls: int = 0
    cost: float = 0.0
    repeated_state_count: int = 0
    trace: List[TraceEvent] = field(default_factory=list)


def stable_action_id(task_id: str, proposal: Proposal, action_version: str = "v1") -> str:
    canonical = f"{task_id}|{proposal.action}|{sorted(proposal.arguments.items())}|{action_version}"
    return sha256(canonical.encode("utf-8")).hexdigest()[:20]


def stop_if_budget_exhausted(state: LoopState) -> Optional[str]:
    t = state.task
    if state.step > t.max_steps:
        return "max_steps"
    if state.tool_calls > t.max_tool_calls:
        return "max_tool_calls"
    if state.model_calls > t.max_model_calls:
        return "max_model_calls"
    if state.cost > t.max_cost:
        return "max_cost"
    if state.repeated_state_count >= t.max_repeated_states:
        return "repeated_state"
    return None


class LoopEngine:
    """Deterministic controller around model, tool and verifier callables."""

    def __init__(
        self,
        observer: Callable[[LoopState], Observation],
        decider: Callable[[LoopState, Observation], Proposal],
        policy: Callable[[LoopState, Proposal], Tuple[bool, str]],
        actor: Callable[[LoopState, Proposal, str], Dict[str, Any]],
        verifier: Callable[[LoopState, Proposal, Dict[str, Any]], bool],
        recover: Optional[Callable[[LoopState, str], Outcome]] = None,
    ) -> None:
        self.observer = observer
        self.decider = decider
        self.policy = policy
        self.actor = actor
        self.verifier = verifier
        self.recover = recover or self._default_recover

    def run(self, state: LoopState) -> LoopState:
        while state.phase not in {Phase.COMPLETE, Phase.STOP, Phase.ESCALATE}:
            stop_reason = stop_if_budget_exhausted(state)
            if stop_reason:
                state.phase = Phase.STOP
                state.stop_reason = stop_reason
                state.result = "safe_stop"
                self._record(state, Phase.STOP, reason=stop_reason)
                break
            state.step += 1

            state.phase = Phase.OBSERVE
            obs = self.observer(state)
            state.observation = obs
            state.state_version = obs.state_version
            self._record(state, Phase.OBSERVE, observation_id=obs.observation_id, fresh=obs.fresh)
            if not obs.fresh:
                state.phase = Phase.RECOVER
                self._record(state, Phase.RECOVER, reason="stale_observation")
                if self.recover(state, "stale_observation") == Outcome.ESCALATE:
                    state.phase = Phase.ESCALATE
                    state.result = "human_escalation"
                    break
                continue

            state.phase = Phase.DECIDE
            state.model_calls += 1
            proposal = self.decider(state, obs)
            state.proposal = proposal
            self._record(state, Phase.DECIDE, action=proposal.action, arguments=proposal.arguments)

            state.phase = Phase.POLICY
            allowed, reason = self.policy(state, proposal)
            self._record(state, Phase.POLICY, allowed=allowed, reason=reason)
            if not allowed:
                state.phase = Phase.ESCALATE
                state.result = "policy_denied"
                state.stop_reason = reason
                break

            action_id = stable_action_id(state.task.task_id, proposal)
            state.last_action_id = action_id
            if action_id in state.completed_action_ids:
                state.phase = Phase.VERIFY
                result = {"deduplicated": True, "action_id": action_id}
            else:
                state.phase = Phase.ACT
                state.tool_calls += 1
                result = self.actor(state, proposal, action_id)
                self._record(state, Phase.ACT, action_id=action_id, result=result)

            state.phase = Phase.VERIFY
            ok = self.verifier(state, proposal, result)
            self._record(state, Phase.VERIFY, ok=ok, action_id=action_id)
            if ok:
                state.verified = True
                state.completed_action_ids.add(action_id)
                state.phase = Phase.COMPLETE
                state.result = "verified_success"
                break

            state.phase = Phase.RECOVER
            outcome = self.recover(state, "verification_failed")
            self._record(state, Phase.RECOVER, outcome=outcome.value)
            if outcome == Outcome.ESCALATE:
                state.phase = Phase.ESCALATE
                state.result = "human_escalation"
                break
            if outcome == Outcome.STOP:
                state.phase = Phase.STOP
                state.result = "safe_stop"
                break
            state.repeated_state_count += 1 if outcome == Outcome.RECOVER else 0

        return state

    @staticmethod
    def _default_recover(state: LoopState, reason: str) -> Outcome:
        if reason == "stale_observation":
            return Outcome.RECOVER
        if state.repeated_state_count >= state.task.max_repeated_states - 1:
            return Outcome.ESCALATE
        return Outcome.REPLAN

    @staticmethod
    def _record(state: LoopState, phase: Phase, **detail: Any) -> None:
        state.trace.append(TraceEvent(phase=phase, detail=detail))


__all__ = ["LoopEngine", "LoopState", "Task", "Observation", "Proposal", "Phase", "Outcome", "stable_action_id"]
