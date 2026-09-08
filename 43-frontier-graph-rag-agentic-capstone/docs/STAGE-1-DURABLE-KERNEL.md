# Stage 1 — Durable Execution Kernel

## Objective

Convert an in-memory agent into a restartable workflow.

## Failure model

Assume any of these can happen after any action:

- worker process dies
- machine restarts
- network request times out
- model call succeeds but response is not persisted
- tool succeeds but worker crashes before recording success
- duplicate queue delivery occurs
- human approval arrives hours later

## Required invariants

1. Every run has a stable `run_id`.
2. State is persisted before it is treated as durable.
3. Consequential actions have idempotency keys.
4. Checkpoints can reconstruct execution state.
5. Cancellation is persisted.
6. Resource budgets are enforced outside the model.
7. Audit events are append-only and structured.
8. Recovery must not blindly repeat an unknown side effect.

## Lab sequence

### Lab A — Crash after action

Create a tool that reports success and then simulate a worker crash before the result is stored.

Question: should recovery retry the tool, reconcile its state, or escalate?

### Lab B — Duplicate delivery

Deliver the same task twice.

Prove that the idempotency key prevents duplicate execution of the same side effect.

### Lab C — Resume

Persist a checkpoint after step 3, terminate the process, reload the run and continue from step 4.

### Lab D — Budget exhaustion

Exhaust step, token, tool-call and cost budgets independently.

### Lab E — Audit reconstruction

Given only the run record and audit log, reconstruct:

```text
what happened?
when?
which tool acted?
what policy decision occurred?
what was verified?
why did the run stop?
```

## Production upgrade

The JSON implementation is intentionally educational. Replace it later with a transactional datastore and durable queue while preserving the same conceptual contracts.

## Mastery test

You pass Stage 1 when you can kill the worker at arbitrary points and explain exactly what the system will do after restart without relying on model memory.
