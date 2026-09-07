from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Callable

class Risk(str, Enum): LOW='low'; MEDIUM='medium'; HIGH='high'

@dataclass(frozen=True)
class PlanStep:
    step_id: str
    objective: str
    dependencies: tuple[str, ...] = ()
    risk: Risk = Risk.LOW
    tool: str | None = None

@dataclass
class Plan:
    plan_id: str
    steps: list[PlanStep]
    version: int = 1

@dataclass(frozen=True)
class Approval:
    task_id: str
    action_hash: str
    approver: str
    approved: bool

class PlanError(ValueError): pass

def validate_plan(plan: Plan) -> None:
    ids={s.step_id for s in plan.steps}
    if len(ids)!=len(plan.steps): raise PlanError('duplicate step id')
    graph={s.step_id:set(s.dependencies) for s in plan.steps}
    if any(dep not in ids for deps in graph.values() for dep in deps): raise PlanError('missing dependency')
    visiting=set(); visited=set()
    def dfs(n):
        if n in visiting: raise PlanError('dependency cycle')
        if n in visited: return
        visiting.add(n)
        for d in graph[n]: dfs(d)
        visiting.remove(n); visited.add(n)
    for n in graph: dfs(n)

def action_hash(task_id: str, step: PlanStep) -> str:
    return sha256(f'{task_id}|{step.step_id}|{step.objective}|{step.tool}'.encode()).hexdigest()

class PlannerExecutor:
    def __init__(self, execute: Callable[[PlanStep], object], verify: Callable[[PlanStep, object], bool]):
        self.execute, self.verify = execute, verify

    def run(self, task_id: str, plan: Plan, approvals: dict[str, Approval] | None = None) -> list[object]:
        validate_plan(plan); done=set(); outputs=[]; approvals=approvals or {}
        while len(done)<len(plan.steps):
            progress=False
            for step in plan.steps:
                if step.step_id in done or not set(step.dependencies)<=done: continue
                if step.risk is Risk.HIGH:
                    a=approvals.get(step.step_id)
                    if not a or not a.approved or a.task_id!=task_id or a.action_hash!=action_hash(task_id,step):
                        raise PermissionError(f'approval required: {step.step_id}')
                result=self.execute(step)
                if not self.verify(step,result): raise RuntimeError(f'verification failed: {step.step_id}')
                outputs.append(result); done.add(step.step_id); progress=True
            if not progress: raise PlanError('no executable progress')
        return outputs
