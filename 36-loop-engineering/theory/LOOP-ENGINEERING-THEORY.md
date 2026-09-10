# Module 36 — Loop Engineering Theory

## 1. Why loop engineering is a core architecture layer

An agent is not made reliable by adding a better prompt or a larger model. The model produces a **proposal**; the loop determines whether that proposal can become an action, whether the action produced the intended effect, and what happens next.

Module 14 introduced the raw agent loop. Module 36 goes one architectural level deeper: it treats the loop as a **deterministic execution kernel** that surrounds probabilistic model decisions. Module 37 then packages these semantics into a reusable harness.

The core invariant is:

> **Untrusted model proposal → deterministic policy/control → bounded side effect → independent verification → explicit recovery or termination.**

This separation is essential because persistence, tools, memory, multi-step execution and external side effects create failure modes that a single model call cannot control.

---

## 2. Core architecture

```text
                         TASK CONTRACT
                              │
                              ▼
                       ┌────────────┐
                       │   OBSERVE  │◄──────────────┐
                       └─────┬──────┘               │
                             │ evidence             │
                             ▼                       │
                       ┌────────────┐               │
                       │   DECIDE   │  model        │
                       │ / PROPOSE  │  proposal     │
                       └─────┬──────┘               │
                             │ typed proposal       │
                             ▼                       │
                       ┌────────────┐               │
                       │   POLICY   │               │
                       │ authority  │               │
                       │ risk/budget│               │
                       └─────┬──────┘               │
                             │ allowed              │
                             ▼                       │
                       ┌────────────┐               │
                       │    ACT     │──────────┐    │
                       │ action GW  │          │    │
                       └─────┬──────┘          │    │
                             │ effect          │    │
                             ▼                 │    │
                       ┌────────────┐          │    │
                       │   VERIFY   │          │    │
                       │postcondition│         │    │
                       └─────┬──────┘          │    │
                         ┌───┴────┐             │    │
                    success      failure       │    │
                       │            │           │    │
                       ▼            ▼           │    │
                   COMPLETE      RECOVER ──────┘    │
                                    │                │
                         ┌──────────┼─────────┐      │
                         ▼          ▼         ▼      │
                       REOBSERVE   REPLAN    STOP    │
                         │          │         │      │
                         └──────────┴─────────┘      │
                                                    │
                    CONTROL PLANE ─────────────────┘
          identity • tenant • policy • approval • budget
          deadline • concurrency • checkpoint • kill switch
          audit • trace • idempotency • evaluation
```

### Control plane vs data plane

**Control plane:** identity, tenant scope, authorization, policy, approval, budgets, deadlines, concurrency, checkpoints, cancellation, kill switch, audit and evaluation. These are authoritative and must not be rewritten by model output, retrieved text, memory or tool output.

**Data plane:** user content, retrieved documents, memory records, observations and tool results. These can influence a decision but are untrusted inputs to the control plane.

---

## 3. The components — what each one owns

### 3.1 Task contract

Defines objective, tenant, allowed capabilities and hard limits before the loop starts.

**Owns:** task identity, scope, maximum steps, model/tool-call limits, cost budget and termination policy.

**Failure if absent:** the agent has no authoritative definition of completion or resource bounds.

### 3.2 Observation layer

Obtains current external evidence. An observation should carry identity, source, freshness, provenance and state version.

**Owns:** evidence acquisition and normalization; it does not decide what the evidence means.

**Deep issue:** stale observations can make a correct action become incorrect. Therefore freshness is a control input, not merely metadata.

### 3.3 Decision / proposal layer

The model converts objective + observations + state into a typed proposed action.

**Owns:** reasoning/proposal generation.

**Does not own:** authority, tenant identity, budget, approval or truth of completion.

This is the key deterministic/probabilistic boundary.

### 3.4 Policy gate

Evaluates whether the proposal is permitted under authoritative rules.

Typical predicates:

```text
identity valid
AND tenant matches
AND action allowed
AND data scope allowed
AND risk threshold satisfied
AND budget available
AND approval present when required
AND deadline valid
```

A policy denial is normally **not a retryable model error**. Repeatedly asking the model to produce a forbidden action is a control failure.

### 3.5 Action gateway

The only controlled path from a proposal to an external side effect.

**Responsibilities:** schema validation, canonicalization, authorization, action identity, idempotency, timeout, rate limiting, logging and side-effect classification.

### 3.6 Verification layer

Checks whether the intended postcondition is actually true.

Verification should be independent enough to catch model self-confirmation. A useful hierarchy is:

```text
L0  model claim
L1  same-source confirmation
L2  independent observation/query
L3  deterministic invariant/verifier
L4  human adjudication for high-impact cases
```

The required level depends on risk.

### 3.7 Recovery controller

Maps failures to explicit actions rather than a generic “try again”.

```text
transient timeout       → bounded retry
rate limit              → backoff/retry
stale evidence          → reobserve
malformed proposal      → repair/reject
policy denial           → stop/escalate
unknown side effect     → reconcile
verification failure    → recover/replan
repeated no-progress    → stop/escalate
worker crash            → resume from checkpoint
budget exhausted        → safe stop
```

### 3.8 State and state versions

State is the memory of the execution kernel: phase, observation, proposal, action identity, verification, counters, cost and trace. A monotonic state version prevents stale branches from overwriting newer authoritative state.

### 3.9 Action identity and idempotency

A stable action ID makes retries distinguishable from duplicate side effects.

```text
action_id = H(task_id + action + canonical_arguments + action_version)
```

A timeout after a write creates **UNKNOWN**, not automatically FAILURE. The system must reconcile external state before deciding whether another write is safe.

### 3.10 Budgets and deadlines

A loop has several independent budgets:

- steps / iterations
- model calls
- tool calls
- tokens
- money
- wall-clock time
- high-risk actions

The model may see remaining budget but cannot increase authoritative limits.

### 3.11 Termination and stop semantics

Termination is a first-class architecture decision. Stop conditions include verified completion, hard budget exhaustion, deadline expiry, repeated-state detection, policy denial, unrecoverable dependency failure and explicit cancellation.

A safe stop should leave an auditable reason and enough state to resume or investigate when appropriate.

### 3.12 Checkpoint and recovery boundary

Checkpoint **semantic state**, not just an iteration counter. A useful checkpoint records task identity, tenant, state version, phase, approved action, action IDs, committed side effects, verification state, remaining budgets and recovery position.

### 3.13 Trace / audit trajectory

Every transition should be explainable through a trajectory containing at least:

```text
run_id, task_id, tenant, state_version, phase,
observation reference, proposal, policy decision,
action_id, tool result summary, verifier result,
error class, latency, token/cost data, stop reason
```

### 3.14 Concurrency and cancellation

Concurrent work introduces stale commits, duplicate effects and races. Use serialization, leases or optimistic version checks as appropriate.

Cancellation is a control event: stop accepting new work, interrupt safe operations, prevent new side effects, record the reason and preserve a resumable checkpoint where policy permits.

---

## 4. State-machine semantics

The loop should be designed as an explicit state machine rather than an implicit `while True` block.

| Transition | Required condition | Failure response |
|---|---|---|
| START → OBSERVE | valid task contract | reject task |
| OBSERVE → DECIDE | fresh/in-scope evidence | reobserve/escalate |
| DECIDE → POLICY | typed proposal | repair/reject |
| POLICY → ACT | authorization + budget + approval | deny/escalate |
| ACT → VERIFY | action result recorded | reconcile if unknown |
| VERIFY → COMPLETE | independent postcondition true | complete |
| VERIFY → RECOVER | postcondition false/unknown | recover/replan |
| RECOVER → OBSERVE | recovery requires new evidence | observe |
| RECOVER → STOP | unsafe/unrecoverable | safe stop |
| RECOVER → ESCALATE | human decision required | escalate |

The architecture therefore makes **illegal transitions visible and testable**.

---

## 5. Loop strategies and trade-offs

### Fixed workflow

```text
A → B → C → D
```

Best when the process is known and deterministic. Lowest variance and easiest to audit; poor fit for uncertain tasks.

### Reactive loop

```text
Observe → Decide → Act → Observe → ...
```

Adapts to the environment but can oscillate or spend excessive resources.

### Guarded adaptive loop

```text
Observe → Decide → Policy → Act → Verify
                     ↑              │
                     └── Recover ───┘
```

Adds explicit budgets, verification, progress signals and recovery policy. This is the default production-oriented pattern taught here.

### Search-based control

Tree search / MCTS can explore alternatives, but expands compute and state-management complexity. The student should learn to justify when search is worth the additional cost and verification burden rather than treating “more reasoning” as automatically better.

---

## 6. Loop pathologies

### Infinite loop
The agent never reaches a terminal state. Defenses: hard step limit, deadline, progress test and repeated-state detection.

### Oscillation
Two or more states/actions alternate without progress. Detect recurring fingerprints and escalate or change strategy.

### Plan churn
The agent repeatedly replaces its plan without producing verified progress. Track plan versions and require progress evidence before replanning again.

### Retry storm
A transient error becomes a cost explosion. Use bounded retries, exponential backoff, jitter and circuit breaking.

### Verification blindness
The loop accepts a self-reported success. Require independent postconditions for meaningful actions.

### Side-effect duplication
A timeout is interpreted as failure and the same write is repeated. Use stable action identity and reconciliation.

### Stale-state overwrite
A slow branch commits after a newer state exists. Use state versions, leases or compare-and-swap semantics.

### Budget bypass
Retrieved text or model output attempts to raise limits. Budgets belong to the control plane and must be immutable to untrusted data.

---

## 7. Engineering metrics

Measure the loop as a system, not just the final answer:

```text
verified task success
unsafe-action acceptance
verification failure rate
recovery success rate
escalation rate
iterations / successful task
tool calls / successful task
model calls / successful task
cost / successful task
p50 / p95 / p99 latency
retry rate
unknown-side-effect rate
loop-pathology rate
checkpoint recovery success
```

A loop optimization is not an improvement if it increases unsafe acceptance or cost per verified success.

---

## 8. Security model

Treat **user input, retrieved documents, memory and tool output as data, not policy**. They can propose facts or actions but cannot redefine:

- identity
- tenant
- permissions
- approval requirements
- budget
- safety policy
- termination rules

High-impact actions should bind approval to the exact action identity and canonical arguments. Audit records should capture the policy decision and verification result without storing unnecessary sensitive payloads.

---

## 9. Production design checklist

Before calling a loop production-ready, ask:

1. What is the authoritative task contract?
2. What evidence is fresh enough to act on?
3. What exactly can the model propose?
4. Where is policy enforced outside the model?
5. What is the only action gateway?
6. How is each side effect identified and deduplicated?
7. What proves completion independently?
8. Which failures retry, recover, reconcile, stop or escalate?
9. What are the hard budgets and deadlines?
10. How is cancellation propagated?
11. What happens after a worker crash?
12. Can a stale branch overwrite newer state?
13. Can the trajectory be replayed and audited?
14. Which metrics prove improvement?
15. Which adversarial cases must fail safely?

## 10. Relationship to adjacent modules

```text
M14 Raw Agent Loop
       ↓ mechanism
M15 Memory ── state that persists across tasks
M16 LangGraph ── explicit workflow/state graph
M17 Planning ── plan generation and replanning
M18 Security ── policy/trust boundary
M20–22 Multi-Agent ── distributed loops and coordination
       ↓
M36 Loop Engineering
       ↓ deterministic execution semantics
M37 Harness Engineering
       ↓ reusable operational wrapper
M38 Long-Running Agents
       ↓ durable execution over time
M39 Skills/Memory/Continual Harnesses
M40 Environments/Verifiers
M41 Self-Improvement
M42 Computer Use
M43 Frontier Graph-RAG Agentic Capstone
```

**Key distinction:** M36 answers *“What must a safe, bounded, verifiable agent loop mean?”* M37 answers *“How do we package those semantics into a reusable harness?”* M38 answers *“How do we keep that execution alive across crashes, leases and long time horizons?”*

## Mastery standard

A student has mastered Module 36 only when they can draw the state machine, explain every control boundary, implement the loop without a framework, inject failures, prove idempotency and independent verification, measure cost/latency/safety trade-offs, and defend why the chosen loop strategy is appropriate for the workload.
