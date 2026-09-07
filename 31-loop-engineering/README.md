# Module 31 — Loop Engineering

## Mission

Learn to engineer the **agent control loop** rather than merely calling an agent framework.

The learner builds a Production Agent Loop Engine that makes every iteration explicit:

```text
Goal
 ↓
Observe
 ↓
Decide
 ↓
Act
 ↓
Observe result
 ↓
Verify
 ├── success → finish
 ├── recoverable failure → recover/replan
 └── budget/deadline/security failure → stop/escalate
```

## Why loop engineering matters

A tool-calling demo often hides the most important questions:

- Who decides the next step?
- What state is carried forward?
- What stops the loop?
- What happens when a tool lies or fails?
- How are retries different from new reasoning steps?
- How much can one task spend?
- How do we know the task is complete?

The loop is where model uncertainty becomes system behavior.

## Learning outcomes

You will be able to:

1. Implement an agent loop from scratch.
2. Separate model decisions from deterministic runtime control.
3. Implement iteration, time, token, tool-call and monetary budgets.
4. Design explicit termination conditions.
5. Implement retries without confusing retry with reasoning.
6. Add reflection and verification without creating infinite loops.
7. Implement checkpoint/recovery semantics.
8. Compare fixed workflows, model-controlled loops and hybrid loops.
9. trace every iteration.
10. diagnose loops that are correct locally but fail globally.

## 1. Three control models

### Deterministic workflow

```text
A → B → C → D
```

Best when the business process is known.

### Model-controlled loop

```text
observe → model decides → tool → observe → model decides ...
```

Useful when the path is genuinely uncertain.

### Hybrid loop

```text
policy/runtime
     ↓
model proposes next action
     ↓
deterministic validation
     ↓
tool execution
     ↓
verifier
     ↓
continue/stop
```

This is the default production pattern for high-control systems.

## 2. The state machine

Represent state explicitly:

```python
from dataclasses import dataclass, field

@dataclass
class AgentState:
    goal: str
    observations: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    iteration: int = 0
    tool_calls: int = 0
    completed: bool = False
```

Do not let state exist only inside an opaque prompt.

## 3. Budget model

A production loop has multiple budgets:

```text
iteration_budget
        + time_budget
        + token_budget
        + tool_budget
        + monetary_budget
        + risk budget
        + concurrency budget
```

The first exhausted hard limit should produce an explicit outcome.

Example:

```text
SUCCESS
FAILED
TIMEOUT
BUDGET_EXCEEDED
POLICY_BLOCKED
HUMAN_REQUIRED
```

## 4. Termination is a design problem

Bad stopping condition:

> “Stop when the model thinks the answer is good.”

Better:

```text
stop if:
  verifier.success
  OR deadline exceeded
  OR iteration budget exhausted
  OR policy violation
  OR human approval required
```

For some tasks, use both model confidence and deterministic verification. Never use confidence alone for high-impact actions.

## 5. Retry vs replan

These are different:

**Retry:** repeat the same operation because failure is transient.

**Replan:** change the strategy because the current path is no longer viable.

```text
Tool timeout
   ↓
retry same call

Tool says resource unavailable
   ↓
replan with another tool/path
```

Conflating these creates loops that burn budget without learning anything.

## 6. Reflection loops

Reflection can help, but every extra model call costs latency and money.

```text
Draft
 ↓
Critique
 ↓
Revision
 ↓
Verify
```

Only retain reflection when experiments show it improves task success enough to justify its cost.

## 7. Maker-checker architecture

A powerful control pattern is:

```text
Generator
   ↓
Candidate action
   ↓
Verifier / critic
   ↓
Policy
   ├── reject
   ├── revise
   └── execute
```

Keep the verifier as independent as practical. If generator and verifier share the same failure mode, apparent confidence can be misleading.

## 8. Build the loop engine

Implement these interfaces:

```python
class Model:
    async def decide(self, state): ...

class Tool:
    async def execute(self, arguments): ...

class Verifier:
    async def verify(self, state, result): ...

class Policy:
    def authorize(self, action): ...
```

Then implement:

```text
AgentRuntime.run(goal)
```

Required controls:

- maximum iterations
- deadline
- cancellation
- tool-call limit
- tool argument validation
- authorization
- verification
- structured trace
- checkpoint after meaningful transitions

## 9. Failure laboratory

Break the engine intentionally:

1. Remove the iteration limit.
2. Make a tool return the same failure forever.
3. Make the model alternate between two actions.
4. Make the verifier always approve.
5. Make the verifier always reject.
6. Drop state between iterations.
7. Let a tool return malformed data.
8. Make the model request an unauthorized tool.
9. Exhaust token budget halfway through a task.
10. Crash after a tool executes but before state is persisted.

For every failure record:

```text
symptom
trace evidence
root cause
control that should have prevented it
regression test
```

## 10. Benchmark

Compare:

- fixed workflow
- simple agent loop
- reflection loop
- verified loop

Measure:

- task success
- iterations/task
- tool calls/task
- p95 latency
- tokens/task
- cost/task
- failure recovery rate

The winning architecture is the one with the best **task-level economics and reliability**, not the most sophisticated loop.

## Interview challenges

1. Design a loop that cannot run forever.
2. What belongs in code versus the model?
3. Why is a retry not the same as a replan?
4. How do you verify an agent's claim of success?
5. How do you recover after a crash immediately after an external side effect?
6. How would you budget a 30-minute autonomous task?
7. When is reflection harmful?
8. Design a loop for a financial action requiring human approval.

## Mastery gate

Build a loop that completes a multi-step task, survives transient tool failure, stops on policy violation, persists checkpoints, and produces a complete trace. Demonstrate that it cannot exceed configured iteration, time, tool and cost budgets.
