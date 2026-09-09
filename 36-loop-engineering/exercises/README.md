# Module 36 Exercises — Loop Engineering

**Purpose:** turn the loop contract into an executable, testable engineering artifact. Do not start with a framework.

## Exercise 1 — Loop Contract v1

For one multi-step task define:
- goal and success criteria
- tenant/resource scope
- authoritative observations and freshness limits
- allowed proposal types
- policy and approval gates
- side effects and verification postconditions
- progress signal
- recovery paths
- stop/escalation conditions

**Deliverable:** one-page contract + state-transition table.

## Exercise 2 — State-machine invariants

Implement explicit states and reject invalid transitions. Test at least:
- stale observation → act
- unapproved high-risk action → execute
- action without recorded attempt → verify
- failed verification → complete
- unknown side effect → blind retry

**Deliverable:** transition tests and invariant matrix.

## Exercise 3 — Typed proposal firewall

Generate valid and malicious proposals. Reject:
- unknown action
- malformed arguments
- wrong tenant
- out-of-scope resource
- fabricated approval
- budget increase
- policy override

**Deliverable:** acceptance/rejection matrix with reason codes.

## Exercise 4 — Observation quality

Build a simulator with fresh, stale, incomplete, wrong-scope and degraded-source observations.

**Measure:** stale-action prevention, re-observation rate and false rejection rate.

## Exercise 5 — Retry vs replan vs reconcile

Simulate transient timeout, rate limit, validation error, authorization denial, dependency outage, stale evidence and unknown side effect.

Prove that each failure reaches the correct path and that retries are bounded by task budget/deadline.

## Exercise 6 — Idempotent side effects

Inject a crash or timeout after a write may have committed. Use an action identity plus reconciliation to prove that recovery cannot create a duplicate external effect.

**Gold property:** one logical action produces at most one committed side effect.

## Exercise 7 — Verification ladder

Compare:
1. model self-report
2. same-source confirmation
3. independent query
4. invariant-based verifier
5. human confirmation for high-risk outcomes

Measure false acceptance, latency and cost.

## Exercise 8 — Loop pathology detector

Create fixtures for:
- repeated state
- repeated action
- A↔B oscillation
- tool ping-pong
- plan churn
- no evidence gain

Explain false positives and why a hard step limit alone is insufficient.

## Exercise 9 — Budget and deadline controller

Implement independent limits for:
- iterations
- model calls
- tool calls
- retrieval calls
- tokens
- wall time
- estimated cost
- high-risk actions

Prove that model output cannot increase a limit.

## Exercise 10 — Checkpoint/recovery matrix

Crash at:
- after observation
- before side effect
- after side effect
- after verification

For each boundary specify resume state, reconciliation requirement and duplicate-side-effect protection.

## Exercise 11 — Concurrency and stale commits

Run two branches from the same state version. Introduce a newer authoritative commit. Reject the stale branch and record the conflict.

Compare optimistic concurrency, leasing and serialization.

## Exercise 12 — Cancellation and deadline propagation

Design cancellation as a control event. Demonstrate:
- no new work after cancellation
- interruptible work is cancelled
- new side effects are blocked
- cancellation cause is persisted
- safe resume semantics are explicit

## Exercise 13 — Replayable trajectory

Define a structured trajectory schema and reconstruct an incident from it.

Minimum fields: run/task/tenant IDs, state version, phase, observation reference, proposal, policy decision, action ID, verifier result, error class, latency, cost and stop reason.

## Exercise 14 — Differential architecture benchmark

Use identical fixtures to compare:
- fixed workflow
- reactive loop
- guarded adaptive loop

Measure verified success, unsafe acceptance, recovery, tool calls/success, p95 latency, cost/success, escalation and pathology rate.

Do not optimize one metric in isolation.

## Exercise 15 — Failure-injection day

Inject at least 16 failures:
provider outage, stale observation, timeout, rate limit, duplicate delivery, malformed action, policy denial, authorization denial, budget exhaustion, deadline expiry, false verifier, worker crash, corrupted checkpoint, prompt injection, poisoned tool output and unknown side effect.

For every case record:
1. detection signal
2. containment boundary
3. retry/recover/replan/stop decision
4. expected user-visible result
5. residual risk
6. evidence captured
7. regression test

## Exercise 16 — Industry loop design

Choose one:
- SOC investigation
- SRE remediation
- coding-agent repair
- banking reconciliation
- governed customer support

Produce a production loop contract and defend every state transition.

## Exercise 17 — 10,000-alert SOC system design

Design an autonomous SOC investigator for 10,000 alerts/day. Defend concurrency, tenant isolation, evidence freshness, approval gates, idempotency, verification, budgets, recovery and auditability.

## Exercise 18 — Reflection economics

Compare 0, 1, 2 and 3 reflection/replanning rounds. Measure **verified improvement per added cost**. Stop when additional reasoning does not justify its measured benefit.

## Exercise 19 — Framework translation

After implementing the mechanism, map it to one workflow/agent framework. Identify exactly which guarantees come from your own loop contract versus the framework.

## Exercise 20 — Module 37 handoff

Submit **Loop Contract v1**:
1. state model
2. transition table
3. action schema
4. policy insertion points
5. verification/postconditions
6. retry taxonomy
7. action identity/idempotency
8. budget/deadline rules
9. stop/escalation rules
10. checkpoint boundaries
11. trajectory schema
12. failure matrix
13. benchmark fixtures

Module 37 must be able to implement the reusable harness without redefining the loop semantics.
