# Module 33 — Long-Running & Autonomous Agents

## Mission

Move from request/response agents to durable workers that can operate for hours or days while remaining bounded, observable, recoverable and governable.

Modern persistent-agent systems make this a practical engineering problem. Grok Bot, for example, describes bots with their own cloud computer, persistent work across applications and explicit return-to-human approval points. The lesson is not to copy a product; it is to understand the architecture required when work continues after the initiating conversation ends.

## Core model

```text
Human delegates goal
        ↓
Create durable run
        ↓
Schedule / queue
        ↓
Execute bounded work
        ↓
Checkpoint
        ↓
Observe / verify
        ↓
Continue / pause / escalate
        ↓
Final artifact + audit record
```

## Learning outcomes

Build a worker that supports:

- durable jobs
- leases/heartbeats
- deadlines
- checkpoints
- retries
- idempotency
- pause/resume
- human escalation
- scheduled execution
- artifact management
- crash recovery
- budget enforcement

## 1. Why long-running agents are different

A chat agent can often fail by producing a bad answer. A persistent worker can:

- repeat an action
- accumulate stale state
- consume an unbounded budget
- continue after a user changes their mind
- act with credentials long after authorization changes
- create duplicate side effects after restart

Therefore lifecycle engineering becomes part of correctness.

## 2. Job lifecycle

```text
CREATED
  ↓
QUEUED
  ↓
RUNNING
  ↓
CHECKPOINTED
  ├── PAUSED
  ├── WAITING_APPROVAL
  ├── RETRYING
  ├── FAILED
  └── COMPLETED
```

Use explicit states. Do not infer lifecycle from logs.

## 3. Heartbeats and leases

A worker should periodically prove it is alive.

If the worker disappears:

```text
lease expires
   ↓
job becomes recoverable
   ↓
another worker claims it
```

This requires careful idempotency around external effects.

## 4. Idempotency

Suppose an agent sends an invoice after writing `status=sent`, then crashes before recording success.

On resume it may send the invoice again.

Use an idempotency key:

```text
operation_id = hash(run_id + logical_action_id)
```

Downstream systems should reject duplicate operations safely.

## 5. Approval gates

Human approval should be explicit state:

```text
agent proposes action
       ↓
policy evaluates
       ↓
requires approval
       ↓
WAITING_APPROVAL
       ↓
human approves/rejects
       ↓
resume or terminate
```

Approval must not disappear when the process restarts.

## 6. Change-of-mind semantics

Persistent agents need cancellation semantics.

Questions:

- Can the user revoke a goal?
- What happens to already queued actions?
- What about actions already in flight?
- What state is retained for audit?

Cancellation is a business operation, not merely `task.cancel()`.

## 7. Build project — Durable Worker

Implement:

```text
POST /runs
POST /runs/{id}/pause
POST /runs/{id}/resume
POST /runs/{id}/cancel
GET  /runs/{id}
GET  /runs/{id}/events
```

Back it with a durable store and a worker queue.

Required tests:

- worker crash
- duplicate delivery
- lease expiry
- timeout
- cancellation during tool call
- approval while worker is offline
- restart after checkpoint
- budget exhaustion

## 8. Failure laboratory

### Infinite autonomous work

Remove the deadline and observe cost growth.

### Duplicate side effect

Crash between external action and checkpoint.

### Stale permission

Revoke user permission while a job is paused.

### Lost approval

Restart the service while approval is pending.

### Zombie worker

Simulate a worker that stops heartbeating but continues executing.

## 9. Metrics

Measure:

- successful runs
- completion time
- recovery rate
- duplicate-action rate
- approval wait time
- budget exhaustion
- stale-run rate
- checkpoint recovery time
- human escalation rate

## 10. Mastery gate

Run an autonomous task for at least several execution cycles, kill the worker, restart it, and demonstrate correct recovery without duplicate irreversible side effects. Demonstrate cancellation and approval persistence.
