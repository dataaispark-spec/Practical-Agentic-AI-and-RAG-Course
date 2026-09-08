# Module 36 — Loop Engineering

## Frontier Agent Engineering Track

> **Build the control loop before trusting the agent.**

This module teaches the engineering of repeated model–environment interaction. A modern agent is not merely a prompt plus tools. It is a loop with explicit state, actions, observations, budgets, stopping rules, verification, recovery, and telemetry.

The learner builds a **Production Agent Loop Engine** from first principles and then studies contemporary harness patterns as architectural case studies.

---

# Learning outcomes

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
10. Design reflection without uncontrolled recursive loops.
11. Measure loop efficiency and task success.
12. Debug trajectories to identify wasted work.
13. Compare fixed workflows, model-controlled loops, graph workflows, and harness-controlled loops.
14. Defend loop-engineering trade-offs in interviews and system design.

## Core model

```text
OBSERVE → DECIDE → ACT → VERIFY → RECOVER / CONTINUE / STOP
```

The model proposes decisions; deterministic software enforces budgets, authorization, schema validation, tool allowlists, idempotency, state transitions, audit and termination.

## Hands-on lab — Production Agent Loop Engine

The learner implements explicit planner, executor and verifier interfaces with independently enforced step/time/model/tool/cost budgets; repeated-action detection; checkpoint/recovery; structured telemetry; deterministic verification where possible; and failure injection.

### Experiment matrix

| Dimension | Values |
|---|---|
| max steps | 3 / 10 / 30 |
| reflection | off / on |
| verifier | deterministic / model-assisted |
| retries | 0 / 1 / 2 |
| concurrency | 1 / 5 / 20 |

### Failure-first cases

- infinite loop;
- oscillation;
- false completion;
- retry multiplication;
- budget race;
- stale checkpoint state.

## Production controls

Deadline propagation, idempotency, checkpointing, compensation, circuit breaking, human escalation and audit reconstruction are required design topics.

## Security

The loop must not infer authorization from its own reasoning. Tool access, tenant scope, destructive actions, network egress and budgets remain deterministic control boundaries.

## Mastery gate

A learner passes only after implementing a bounded loop, reproducing at least two injected failures, demonstrating verification-driven termination, measuring efficiency, and defending which decisions belong to the model versus the runtime.
