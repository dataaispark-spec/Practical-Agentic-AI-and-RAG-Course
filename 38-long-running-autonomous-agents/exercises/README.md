# Module 38 Exercises — Durable-Agent Engineering

## Exercise 1 — State-machine specification
Write a transition table for a worker that can run, wait for approval, resume, retry, cancel and dead-letter. For every transition specify precondition, durable write, side effect and recovery behavior.

## Exercise 2 — Exactly-once claim review
A teammate says: "Our queue guarantees exactly-once, so duplicate payments are impossible." Red-team the claim. Separate delivery semantics, execution semantics and business-effect semantics. Propose a safer contract.

## Exercise 3 — Timeout-after-write
An API times out after 4 seconds. The external ledger shows the correction 30 seconds later. Design the effect record lifecycle and reconciliation algorithm. State what happens if the reconciliation API is unavailable too.

## Exercise 4 — Fencing race
Worker A has fence 17. Its network is partitioned. Worker B obtains fence 18. A later attempts a state commit. Draw the timeline and identify the exact enforcement point that must reject A.

## Exercise 5 — Approval replay
An approval is valid for 15 minutes and is bound to an action hash. During the wait, the target account changes and policy moves from P7 to P8. Explain why the old approval cannot authorize execution.

## Exercise 6 — Budget economics
A task starts with a $5 budget. Each model call costs $0.02, each tool call $0.01, and each retry adds 3 tool calls. Build a cumulative budget table for five attempts and define the stop/escalate boundary.

## Exercise 7 — Backpressure
Arrival is 200 events/s and sustainable capacity is 120 events/s. Design admission control, retry policy, tenant fairness and DLQ behavior. Calculate the expected backlog growth before controls.

## Exercise 8 — Disaster recovery
Define RPO/RTO separately for task state, effect ledger, approvals, audit events and derived model summaries. Explain which data may be eventually consistent and which must be strongly protected.

## L7 architecture challenge
Design a multi-region durable-agent platform for 1 million concurrent tasks. Defend storage consistency, leases/fencing, idempotency, event-driven waiting, cancellation, budget enforcement, tenant isolation, observability and failure recovery. Explicitly identify guarantees that are impossible to make universally.

### Submission standard
Every exercise must contain: assumptions → design/derivation → failure case → invariant → evidence → residual risk.