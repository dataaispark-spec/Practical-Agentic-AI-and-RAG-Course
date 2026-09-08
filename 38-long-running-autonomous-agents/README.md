# Module 33 — Long-Running & Autonomous Agents

## Mission

Move from request/response agents to durable workers that can operate for hours or days while remaining bounded, observable, recoverable and governable.

## Core abstraction

```text
Long-running Agent
= Goal + Durable State + Loop + Environment + Tools
  + Policy + Budgets + Verification + Recovery
```

A large context window is not durable execution. Persistence requires an authoritative state model outside model context.

## Learning outcomes

Build and defend workers supporting durable goals/tasks/runs, leases and heartbeats, deadlines, multidimensional budgets, checkpoints, resumability, bounded retries, idempotent side effects, pause/resume/cancel, human escalation, scheduling, artifacts, crash recovery, stale-state detection, policy re-validation and audit reconstruction.

## Hands-on track

Study five identities: GOAL, TASK, RUN, ATTEMPT, CHECKPOINT. Implement a durable lifecycle, worker leases, heartbeat/progress monitoring, idempotency, checkpointing, context compaction, event-driven waiting, approval persistence, change-of-mind semantics, goal-drift detection, multidimensional budgets, recovery matrices and scheduled autonomy.

### Failure-first labs

Break and recover from duplicate execution, split brain, lost progress, goal drift, infinite autonomy, stale policy, stale knowledge, zombie workers and uncertain external side effects.

### Frontier case studies

Analyze Hermes Agent, Prime Agent and Grok Bot as architectural case studies. For each capability ask: **what persistence/control primitive makes it possible, and what new failure mode does it introduce?**

### Production project

Build a Durable Autonomous Worker with a durable queue/state store, leases, checkpoints, policy, budgets, approvals, verification, audit and replay/debugging. Measure completion, recovery, duplicate side effects, recovery time, cost, checkpoint overhead and escalation rate.

### Mastery gate

Demonstrate safe stop/restart/wait/resume behavior, bounded autonomy, no duplicate side effects, policy revalidation and reconstructable execution history.