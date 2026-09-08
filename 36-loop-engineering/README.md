# Module 31 — Loop Engineering

## Frontier Agent Engineering Track

> **Build the control loop before trusting the agent.**

This module teaches the engineering of repeated model–environment interaction. A modern agent is not merely a prompt plus tools. It is a loop with explicit state, actions, observations, budgets, stopping rules, verification, recovery, and telemetry.

The learner builds a **Production Agent Loop Engine** from first principles and then studies contemporary harness patterns as architectural case studies.

---

## 1. Why loop engineering exists

A basic LLM call has one dominant transition:

```text
input → model → output
```

An agent introduces recurrence:

```text
             +-----------------------+
             |                       |
             v                       |
         observe state              |
             |                       |
             v                       |
          decide -------------------+
             |
             v
          act/tool
             |
             v
          observe
```

The dangerous part is the arrow back to the beginning.

Without controls, the system can:

- loop forever
- repeat the same failed action
- consume unlimited tokens
- repeatedly call expensive tools
- mutate external state unnecessarily
- oscillate between plans
- mistake an intermediate result for completion
- continue after the user has disconnected
- retry a destructive operation
- declare success without verification

Therefore:

> **The loop is an engineered runtime contract, not an incidental prompt pattern.**

---

# 2. Learning outcomes

By completing this module you can:

1. Model an agent as a state-transition system.
2. Separate model decisions from deterministic control logic.
3. Implement bounded agent loops from scratch.
4. Design explicit termination conditions.
5. Distinguish retries from reasoning iterations.
6. Add step, time, token, tool, and monetary budgets.
7. Detect repeated-state and repeated-action loops.
8. Add verification before declaring task completion.
9. Implement checkpointing and recovery.
10. Design reflection without creating uncontrolled recursive loops.
11. Measure loop efficiency and task success.
12. Debug traces to identify where an agent is wasting work.
13. Compare fixed workflows, model-controlled loops, graph workflows, and harness-controlled loops.
14. Explain loop-engineering trade-offs in interviews.

---

# 3. Core model: state transition

Represent the agent as:

```text
S_t + Goal + Policy
        |
        v
     Decision
        |
        v
      Action
        |
        v
   Environment
        |
        v
Observation
        |
        v
      S_t+1
```

A useful abstract formulation is:

```text
S(t+1) = transition(S(t), action(t), observation(t))
```

The model proposes decisions; deterministic software should enforce contracts around them.

### Explicit state

```python
from dataclasses import dataclass, field


@dataclass
class LoopState:
    goal: str
    step: int = 0
    status: str = "running"
    observations: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    verified: bool = False
    failure_count: int = 0
```

Do not hide critical state solely inside a prompt transcript.

---

# 4. The five-part production loop

Use this baseline:

```text
OBSERVE
   |
   v
DECIDE
   |
   v
ACT
   |
   v
VERIFY
   |
   +---- success ----> COMPLETE
   |
   +---- failure ----> RECOVER / STOP
   |
   v
OBSERVE again
```

This differs from a simplistic:

```text
think → tool → think → tool → ...
```

because **verification is explicit**.

---

# 5. Deterministic control vs model control

A critical design question is:

> What should the model decide, and what should software enforce?

### Model is good at

- interpreting ambiguous language
- choosing among legitimate strategies
- generating hypotheses
- selecting a tool based on semantic intent
- composing natural-language plans

### Deterministic code should enforce

- maximum steps
- maximum wall-clock time
- authorization
- schema validation
- tool allowlists
- rate limits
- monetary limits
- retry counts
- destructive-action approval
- state transitions
- audit logging
- termination conditions

### Golden rule

```text
Model proposes.
Runtime disposes.
```

The model should not be the final authority over its own safety boundary.

---

# 6. Termination engineering

Every loop needs at least one hard termination mechanism.

Use multiple independent limits:

```text
             LOOP
              |
      +-------+--------+
      |       |        |
    steps    time    budget
      |       |        |
      +-------+--------+
              |
          termination
```

Recommended controls:

- `max_steps`
- `deadline`
- `max_model_calls`
- `max_tool_calls`
- `max_cost`
- `max_repeated_action`
- `max_same_state`
- explicit success condition
- explicit unrecoverable failure condition

Do not rely on “the model will know when to stop.”

---

# 7. A minimal bounded loop

```python
async def run_agent(goal, planner, executor, verifier, max_steps=10):
    state = LoopState(goal=goal)

    while state.status == "running":
        if state.step >= max_steps:
            state.status = "budget_exhausted"
            break

        decision = await planner(state)
        observation = await executor(decision)
        state.observations.append(observation)
        state.actions.append(decision)
        state.step += 1

        result = await verifier(state)
        if result.success:
            state.verified = True
            state.status = "completed"
        elif result.fatal:
            state.status = "failed"

    return state
```

This deliberately keeps the loop understandable.

Later modules can add graphs, planners, memory, sub-agents, MCP and sophisticated harnesses. First understand the primitive.

---

# 8. Retry is not reasoning

This distinction is often missed.

### Retry

The same intended operation is attempted again because of a transient failure.

```text
call API
  ↓
HTTP 503
  ↓
backoff
  ↓
call API again
```

### Reasoning iteration

The system has learned something new and chooses a different action.

```text
search
 ↓
insufficient evidence
 ↓
change query
 ↓
search again
```

Retries belong to **reliability engineering**; reasoning iterations belong to **agent control**.

Combining both without separate budgets can create multiplicative explosions.

---

# 9. Loop budgets

Define budgets independently.

| Budget | Example | Purpose |
|---|---:|---|
| steps | 12 | prevents infinite reasoning |
| model calls | 20 | controls inference |
| tool calls | 30 | controls external actions |
| wall time | 90 s | protects user/request |
| token budget | 50k | controls context/model cost |
| money | $0.50 | protects economics |
| retries | 2 | controls transient failures |
| destructive actions | 0 until approval | protects external state |

A task can exhaust one budget while others remain available. That should be represented explicitly in telemetry.

---

# 10. Detecting loops

A common failure is semantic repetition:

```text
search("customer refund policy")
search("customer refund policy")
search("customer refund policy")
...
```

Exact string comparison is insufficient. Normalize actions and state fingerprints.

```python
import hashlib
import json


def fingerprint(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()[:16]
```

Track recent fingerprints:

```text
state A
state B
state A
state B
state A
```

This can indicate oscillation rather than progress.

---

# 11. Progress metrics

Do not measure only final success.

Track:

```text
success rate
steps/task
model calls/task
tool calls/task
retry count
repeated-action count
verification failures
wall-clock time
cost/task
useful observations/step
```

A powerful metric is:

```text
verified success / total loop work
```

Two agents may have equal success but radically different efficiency.

---

# 12. Verification patterns

## Pattern A — deterministic verifier

Best when possible.

Example:

```text
Agent edits code
      ↓
run tests
      ↓
PASS / FAIL
```

## Pattern B — structured verifier

Check schema, constraints, counts or invariants.

## Pattern C — model judge

Useful when correctness is difficult to compute deterministically, but should be treated as a fallible evaluator.

## Pattern D — hybrid verifier

```text
semantic evaluator
       +
deterministic checks
       +
policy checks
```

The course will prefer deterministic evidence whenever practical.

---

# 13. Reflection loops

Reflection can improve quality:

```text
draft
 ↓
critique
 ↓
revise
 ↓
verify
```

But uncontrolled reflection becomes:

```text
critique → revise → critique → revise → ...
```

Therefore reflection needs:

- maximum reflection rounds
- measurable improvement threshold
- independent evaluator where possible
- cost budget
- stop-on-no-improvement

The threshold should be task-specific and empirically validated.

---

# 14. Planner/executor loops

Separate planning from execution when the task benefits from explicit decomposition.

```text
Goal
 ↓
Planner
 ↓
Plan
 ↓
Executor
 ↓
Observation
 ↓
Verifier
 ↓
Planner / completion
```

But don't create a planner merely because “agents should plan.”

For short tasks, planning overhead may reduce performance. Benchmark:

```text
baseline single-pass
vs
planner + executor
```

Compare task success, latency, cost and failure rate.

---

# 15. Loop architectures

### A. Fixed deterministic workflow

```text
A → B → C → D
```

Best for predictable business processes.

### B. ReAct-style loop

```text
observe → decide → act → observe
```

Flexible but needs strong controls.

### C. Planner/executor

```text
plan → execute → verify
```

Useful for multi-step tasks.

### D. Graph workflow

```text
             ┌── tool A ──┐
start → route ├── tool B ──┼→ verify → end
             └── human ──┘
```

Useful when state transitions should be explicit.

### E. Harness-controlled loop

```text
Model
 ↓
Runtime
 ├─ state
 ├─ tools
 ├─ context
 ├─ policy
 ├─ budgets
 ├─ recovery
 └─ verification
```

This becomes increasingly important for long-running agents.

---

# 16. Frontier connection: Hermes, Prime Agent and modern harnesses

Contemporary agent systems show that the loop increasingly lives inside a richer runtime.

Hermes documents tools/toolsets, persistent memory, skills, checkpoints, scheduled tasks, delegation, MCP and programmatic tool calling. Its MCP guidance also emphasizes least-useful-surface exposure and warns that parallel tool execution is appropriate only when shared-state races are understood. citeturn0search4turn0search1

Prime Agent goes further by treating context as a variable inside a persistent REPL and making prompts, memories, skills and sub-agent specifications durable, editable harness state. Its published research describes explicit execution, recovery, verification and resource accounting around long-horizon tasks. citeturn0search0turn0academia36

The engineering lesson is **not** “use Hermes” or “use Prime Agent.”

The lesson is:

> As model capability increases, the runtime around the model becomes an increasingly important source of system behavior.

This course therefore builds the primitive loop first and studies frontier systems as architectural case studies.

---

# 17. Hands-on lab — Production Agent Loop Engine

## Repository target

```text
31-loop-engineering/
├── README.md
├── labs/
│   └── agent_loop/
│       ├── models.py
│       ├── loop.py
│       ├── budgets.py
│       ├── verifier.py
│       ├── recovery.py
│       ├── telemetry.py
│       └── fake_environment.py
├── tests/
├── exercises/
├── solutions/
├── benchmarks/
└── interview/
```

## Required interfaces

```python
class Planner:
    async def decide(self, state): ...

class Executor:
    async def execute(self, action): ...

class Verifier:
    async def verify(self, state): ...
```

The engine must enforce budgets independently of these components.

### Required experiment matrix

Run:

- max steps: 3 / 10 / 30
- reflection: off / on
- verifier: deterministic / model-based
- retry budget: 0 / 1 / 2
- concurrency: 1 / 5 / 20 where applicable

Record:

```text
task_success
verified_success
steps
model_calls
tool_calls
retries
latency_ms
estimated_cost
failure_reason
```

---

# 18. Failure laboratory

## Failure A — Infinite loop

Inject a planner that repeatedly chooses the same action.

Expected control:

```text
repeated action detected
        ↓
recovery attempt
        ↓
second repetition
        ↓
terminate
```

## Failure B — Oscillation

Make the planner alternate between two actions.

Detect repeating state fingerprints.

## Failure C — False completion

Return a plausible answer without satisfying the actual task.

Verifier must reject it.

## Failure D — Retry multiplication

Make the tool fail transiently while the planner also retries.

Measure the number of actual upstream attempts.

## Failure E — Budget race

Two concurrent sub-operations consume the same global budget.

The budget manager must be atomic.

## Failure F — Stale state

Resume from a checkpoint whose external environment has changed.

The recovery layer must revalidate assumptions before continuing.

---

# 19. Production design patterns

### Deadline propagation

Pass the remaining deadline through every operation.

### Idempotency

Repeated execution must not accidentally duplicate external side effects.

### Checkpointing

Persist enough state to resume safely.

### Compensation

If an action cannot be rolled back, design compensating operations or require approval before execution.

### Circuit breaking

Stop calling a failing dependency rather than repeatedly amplifying failure.

### Human escalation

Escalate when confidence is insufficient, policy requires approval, budget is exceeded, external state is ambiguous, or the action is irreversible/high-risk.

---

# 20. Security

Loop security is broader than prompt injection.

Threats include:

- infinite resource consumption
- tool abuse
- privilege escalation
- confused-deputy behavior
- repeated destructive actions
- poisoned state
- malicious observations
- compromised tools
- cross-tenant state leakage
- unsafe autonomous continuation

Required controls:

```text
identity
 ↓
authorization
 ↓
tool policy
 ↓
budget
 ↓
action validation
 ↓
approval
 ↓
audit
```

Never allow a loop to infer authorization from its own reasoning.

---

# 21. Interview preparation

## Conceptual

1. What makes an agent a loop?
2. Why are explicit termination conditions necessary?
3. What is the difference between retry and reasoning iteration?
4. Why should model decisions be separated from runtime policy?
5. Why is verification a separate phase?
6. When is a deterministic workflow better than an agent loop?
7. What is loop oscillation?
8. How do you detect repeated semantic actions?
9. Why are budgets multidimensional?
10. Why is cost per successful task more useful than cost per request?

## Coding

11. Implement a bounded async agent loop.
12. Add a global step budget.
13. Add a wall-clock deadline.
14. Detect repeated actions.
15. Implement a state fingerprint.
16. Implement a verifier interface.
17. Implement checkpoint/recovery.
18. Implement atomic budget accounting.
19. Add structured loop telemetry.
20. Write tests for cancellation and budget exhaustion.

## Debugging

21. An agent succeeds but uses 10× more tool calls than before. Investigate.
22. p95 latency doubles while model latency remains constant. What do you inspect?
23. A loop alternates between two valid actions forever. Diagnose it.
24. A verifier reports success but the external state is wrong. What is missing?
25. A retry policy causes 900 downstream calls from 100 tasks. Explain the multiplication.

## System design

26. Design a long-running coding agent with a 30-minute deadline.
27. Design a financial operations agent where every side effect needs approval.
28. Design a multi-tenant agent runtime with independent budgets.
29. Design an agent that survives process crashes.
30. Design a verifier architecture for software-engineering tasks.

---

# 22. Mastery gate

You pass Module 31 only when you can build and defend a loop that:

- has explicit state
- separates decision from execution
- enforces hard budgets
- has deterministic termination
- detects repetition
- distinguishes retries from reasoning
- verifies success
- records structured telemetry
- checkpoints safely
- recovers from transient failure
- refuses unauthorized actions
- produces an evidence-backed performance report

### Gold-standard challenge

Build an agent that solves a multi-step task in a simulated environment.

The evaluator will inject:

```text
slow tools
transient errors
repeated observations
misleading observations
partial failures
stale checkpoints
budget pressure
```

The agent must maximize **verified task success per unit of total work**, not simply run until it produces a plausible answer.

---

# 23. Key takeaways

1. Agents are control loops.
2. Loops need budgets.
3. Budgets need enforcement outside the model.
4. Retries and reasoning iterations are different mechanisms.
5. Verification should be explicit.
6. Repetition is an observable failure mode.
7. Persistent state changes the reliability problem.
8. Long-running agents require recovery engineering.
9. The harness increasingly determines how much capability a model can actually express.
10. The right objective is not maximum autonomy; it is **maximum verified useful work within explicit safety, reliability and cost boundaries**.

---

## Frontier reading / case-study references

- Prime Agent — Recursive Language Model + Continual Harness. citeturn0search0turn0academia36
- Prime Agent source implementation and refinement design. citeturn0search3turn0search6
- Hermes Agent — tools, memory, skills, checkpoints, delegation and MCP. citeturn0search4turn0search1
