# Module 21 — Multi-Agent Coordination: Fault-Tolerant Agent Network

## Mission

Move from a supervisor/worker prototype to a distributed agent network that can coordinate under delays, duplicates, crashes, disagreement and partial outages.

**Core principle:** distributed-agent reliability comes from explicit protocols and durable state, not from asking agents to "coordinate better."

## Learning outcomes

You will learn to:

1. Design explicit agent-to-agent message contracts.
2. Use correlation IDs, causation IDs and idempotency keys.
3. Implement task leases, heartbeats and expiry.
4. Handle duplicate, delayed and out-of-order messages.
5. Implement bounded retries and dead-letter handling.
6. Apply backpressure and concurrency limits.
7. Propagate deadlines and cancellation.
8. Use quorum/consensus carefully without confusing agreement with truth.
9. Recover partial failures from durable checkpoints.
10. Debug distributed agent trajectories.

## 1. Distributed agent mental model

A network consists of:

`agents + messages + state + clocks + failures + policies`

Assume the network can produce:

- duplicate delivery;
- delayed delivery;
- reordered delivery;
- lost delivery;
- worker crash;
- coordinator crash;
- stale state;
- network partition;
- overloaded queues;
- conflicting outputs.

Design for these cases from the beginning.

## 2. Message envelope

A production message should carry:

```text
message_id
correlation_id
causation_id
parent_task_id
sender_principal
receiver_principal
tenant_id
schema_version
created_at
expires_at
idempotency_key
payload
security classification
```

The payload must not be allowed to override identity or authorization metadata.

## 3. Idempotency

At-least-once delivery is common and often preferable to silently losing work. Therefore consumers must make operations idempotent where possible.

`operation + idempotency_key → one durable outcome`

For non-idempotent actions, require stronger coordination and approval semantics.

## 4. Leases

A worker can claim a task for a limited period:

`PENDING → LEASED → COMPLETED`

If the lease expires:

`LEASED → RECOVERABLE`

A new worker can reclaim the task only after the previous lease is invalidated or expires.

Use a lease ID to prevent stale workers from committing after ownership changes.

## 5. Heartbeats

Long-running workers periodically report liveness and progress.

Heartbeat fields should include:

- task ID;
- lease ID;
- progress marker;
- remaining deadline;
- consumed budget;
- worker status.

A heartbeat is evidence of liveness—not proof of task correctness.

## 6. Retry taxonomy

Retry:
- transient network failure;
- rate limit;
- temporary dependency outage.

Do not blindly retry:
- authorization denial;
- invalid schema;
- deterministic policy rejection;
- non-idempotent side effect without deduplication;
- expired business deadline.

Use exponential backoff with jitter and a maximum attempt count.

## 7. Backpressure

An autonomous network can amplify load rapidly. Control it with:

- bounded queues;
- concurrency limits;
- per-agent budgets;
- global budgets;
- admission control;
- deadlines;
- cancellation;
- priority classes.

Backpressure is a safety feature, not merely a performance optimization.

## 8. Coordination protocols

### Work queue
Good for independent tasks and durable recovery.

### Fan-out/fan-in
Good for bounded parallel research.

### Lease/claim
Good when multiple workers compete for tasks.

### Quorum
Useful when independent evidence must reach a threshold, but dangerous when failures are correlated.

### Leader/supervisor
Useful for coordination but creates a bottleneck/failure dependency.

### Gossip/pub-sub
Useful for dissemination, but harder to reason about consistency.

## 9. Quorum and consensus

Define the decision property first:

- agreement;
- evidence coverage;
- availability;
- safety;
- conflict detection.

Never assume `3 of 5 agents agree` means truth. If all five consumed the same poisoned retrieval, the errors are correlated.

## 10. Detailed labs

### Lab 1 — Message protocol
Implement versioned envelopes with correlation and causation IDs.

### Lab 2 — Duplicate delivery
Deliver the same message three times. Prove only one durable side effect occurs.

### Lab 3 — Out-of-order messages
Send completion before progress and progress after completion. Add state-machine validation.

### Lab 4 — Lease ownership
Implement task claiming, lease expiry and stale-worker rejection.

### Lab 5 — Heartbeats
Simulate a slow worker and detect a dead worker without killing healthy tasks.

### Lab 6 — Retry policy
Inject transient, permanent and authorization failures. Retry only the appropriate classes.

### Lab 7 — Dead-letter queue
Move exhausted tasks to a dead-letter store with reason and replay metadata.

### Lab 8 — Backpressure
Flood the network with tasks. Measure queue depth and enforce admission control.

### Lab 9 — Cancellation
Cancel a parent task and propagate cancellation to children.

### Lab 10 — Quorum
Compare majority voting with evidence-based verification under correlated failures.

### Lab 11 — Network partition
Simulate a partition and stale state. Define safe behavior when communication resumes.

### Lab 12 — Distributed incident reconstruction
Reconstruct one run from message, worker, tool and policy events.

## 11. Failure injection matrix

| Failure | Expected control |
|---|---|
| duplicate message | idempotency |
| delayed message | expiry/version check |
| stale worker | lease ID |
| worker crash | lease recovery |
| coordinator crash | durable checkpoint |
| queue overload | backpressure |
| transient dependency | bounded retry |
| permanent error | dead letter |
| parent cancellation | propagation |
| partition | safe degraded mode |
| conflicting workers | verifier/escalation |
| poisoned context | trust/security boundary |

## 12. Production state machine

```text
PENDING
  ↓ claim
LEASED ──heartbeat──> LEASED
  ↓ success             ↓ lease expiry
COMPLETED             RECOVERABLE
                         ↓ reclaim
                       LEASED

Any state → CANCELLED when policy permits.
```

State transitions must be validated atomically.

## 13. Observability

Trace:

`run → message → receiver → task → tool → state transition → result`

Useful metrics:

- queue depth;
- oldest message age;
- lease-expiry rate;
- retry rate;
- dead-letter rate;
- duplicate rate;
- stale-commit rejections;
- cancellation latency;
- recovery time;
- coordination messages per successful task.

## 14. Security integration

Every message is a potential trust-boundary crossing.

Enforce:

- authenticated sender;
- authorized receiver;
- tenant binding;
- capability delegation;
- payload schema validation;
- message expiry;
- replay protection;
- security classification;
- audit trail.

A worker cannot grant another worker permissions merely by putting them into a message payload.

## 15. Industry scenarios

**Banking:** payment workflows need durable idempotency and strict state transitions; duplicate delivery must never duplicate money movement.

**Healthcare:** long-running document analysis can tolerate worker failure, but patient-resource access must remain tenant/resource scoped.

**Cybersecurity:** distributed reconnaissance benefits from parallelism while containment actions need stronger approval and lease semantics.

**Enterprise IT:** queue-based diagnostics should survive worker crashes without reopening already completed change actions.

## 16. Interview questions

1. Why is at-least-once delivery often practical for agents?
2. What problem does a lease solve?
3. Why is a heartbeat not verification?
4. How do you reject stale workers?
5. What should be retried?
6. How do you implement backpressure?
7. Why can quorum fail under correlated errors?
8. How do you recover after coordinator failure?
9. What is a dead-letter queue?
10. How do deadlines propagate through a graph?
11. How do you handle out-of-order events?
12. How would you debug duplicate side effects?
13. What should a message envelope contain?
14. How do you secure agent-to-agent delegation?
15. When would you choose a queue over direct RPC?

## 17. System-design challenge

Design a 100-agent enterprise research network handling 10,000 tasks/hour with at-least-once delivery, worker crashes, bounded cost, tenant isolation and 99.9% task completion reliability.

Defend your queueing, leases, retries, backpressure, state model, security and observability choices.

## 18. Coding challenges

- Versioned message envelope
- Idempotency store
- Lease manager
- Heartbeat monitor
- Retry classifier
- Exponential backoff with jitter
- Dead-letter queue
- Bounded admission controller
- Cancellation propagation
- Quorum evaluator
- Stale-commit detector
- Distributed trace correlator

## 19. Mastery gate

You pass when you can demonstrate:

- duplicate-safe execution;
- lease-based ownership;
- stale-worker rejection;
- bounded retry;
- backpressure;
- cancellation propagation;
- dead-letter recovery;
- partition-safe behavior;
- complete distributed tracing.

## Gold challenge

Build **AegisAI Fault-Tolerant Agent Network** with versioned messages, durable queue semantics, leases, heartbeats, idempotency, retries, dead letters, backpressure, cancellation, tenant/capability enforcement and distributed run reconstruction.
