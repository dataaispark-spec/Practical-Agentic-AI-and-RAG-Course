# Module 36 — Loop Engineering

**Canonical implementation:** `36-loop-engineering/`  
**Course position:** Frontier Agent Engineering — Module 36 of 43  
**Previous module:** Module 35 — Compounding Knowledge / LLM Wiki  
**Next module:** Module 37 — Harness Engineering

> **Core thesis:** An agent becomes operational when its loop is engineered as a bounded state machine rather than treated as “call the model again.” The loop must make progress, respect policy, survive faults, verify outcomes, and stop for a reason that can be explained later.

---

## 1. Why this module exists

Earlier modules teach agent foundations, tool calling, workflows, memory, security, evaluation, deployment, and the integrated AegisAI system. Module 36 changes the unit of design.

Instead of starting with a framework, start with the **execution loop**:

```text
OBSERVE
   ↓
DECIDE / PROPOSE
   ↓
POLICY / VALIDATE
   ↓
ACT
   ↓
VERIFY
   ├──────────── success ────────→ COMMIT / COMPLETE
   └──────────── failure ─────────→ RECOVER / REPLAN
                                      ↓
                                   CONTINUE
                                      or
                                     STOP
```

The important distinction is:

- **Model:** proposes a decision or action.
- **Loop:** controls what happens before, during, and after that proposal.
- **Harness (Module 37):** packages the loop into reusable runtime infrastructure.
- **Long-running runtime (Module 38):** makes the controlled execution durable across hours, days, failures, and changing environments.

A good loop therefore behaves more like a small safety-critical controller than a clever prompt.

---

## 2. Learning outcomes

By completing this module, you should be able to:

1. Model an agent as an explicit state machine with valid and invalid transitions.
2. Separate **observation, decision, policy, action, verification, recovery, and termination**.
3. Define progress and detect no-progress, oscillation, repeated-state, and tool-ping-pong pathologies.
4. Convert free-form model output into typed action proposals before execution.
5. Enforce budgets for time, model calls, tool calls, tokens, money, and risky actions.
6. Classify failures into retryable, non-retryable, unknown-side-effect, and escalation paths.
7. Use action identity/idempotency to prevent duplicate side effects.
8. Design independent postconditions instead of trusting model self-reports.
9. Place checkpoints at meaningful side-effect boundaries and recover safely.
10. Build replayable trajectories that explain what was observed, proposed, executed, and verified.
11. Keep untrusted user, retrieval, memory, and tool content from becoming control instructions.
12. Compare fixed workflows, reactive loops, and guarded adaptive loops with measurable evidence.
13. Design cancellation, deadline propagation, kill switches, and safe-stop behavior.
14. Inject failures deliberately and document residual risk rather than only happy-path success.
15. Produce a loop contract that can be handed cleanly to Module 37 for harness implementation.

---

## 3. Prerequisites and continuity

Recommended prerequisites:

- **Module 13:** typed tools and API agents;
- **Module 14:** raw agent loops;
- **Module 15:** memory and persistence risks;
- **Module 17:** planning and human approval;
- **Module 18:** agent security;
- **Module 21:** distributed coordination and fault tolerance;
- **Module 25:** observability;
- **Module 26–29:** production evaluation, cost, governance, deployment;
- **Module 30:** AegisAI enterprise capstone.

Module 36 is deliberately **mechanism-first**. Framework implementation belongs downstream.

---

# 4. The Loop Contract

A production loop should be specified before it is implemented.

### Minimum contract

| Dimension | Question | Example |
|---|---|---|
| Goal | What outcome is required? | Investigate suspicious login |
| Scope | What resources may be touched? | One tenant / one incident |
| Observation | What evidence is authoritative? | SIEM + IAM records |
| Decision | What may the model propose? | Query, enrich, escalate |
| Policy | What is prohibited / gated? | No account disable without approval |
| Action | What effect can occur? | Read event / create ticket |
| Verification | What proves success? | Independent IAM state |
| Progress | What counts as forward motion? | New evidence / completed action |
| Recovery | What happens after failure? | Retry, reconcile, replan, escalate |
| Stop | Why may execution end? | Success, budget, deadline, safety |

A loop without explicit answers to these questions is underspecified.

---

# 5. State-machine design

Do not hide lifecycle state inside a prompt.

A useful baseline is:

```text
START
  ↓
OBSERVE
  ↓
DECIDE
  ↓
POLICY_CHECK
  ├── DENY → SAFE_STOP / ESCALATE
  └── ALLOW
        ↓
      ACT
        ↓
   VERIFY
   ├── PASS → COMMIT → COMPLETE
   └── FAIL
        ↓
     CLASSIFY
   ├── RETRY
   ├── RECOVER
   ├── REPLAN
   └── ESCALATE
```

### Transition invariants

A transition is valid only when its preconditions are satisfied.

Examples:

```text
OBSERVE → DECIDE
requires: sufficiently fresh observation

DECIDE → ACT
requires: typed proposal + policy approval + budget

ACT → VERIFY
requires: recorded action attempt

VERIFY → COMPLETE
requires: independent postcondition evidence

UNKNOWN_SIDE_EFFECT → RETRY
requires: reconciliation or idempotency proof
```

This is the heart of Loop Engineering: **state transitions are contracts, not suggestions.**

---

# 6. Observation engineering

The loop can only be as good as the evidence entering it.

For every observation, capture at least:

```text
observation_id
source
resource_scope
timestamp
freshness / TTL
provenance
confidence / quality
payload hash
```

## 6.1 Freshness

A stale observation can produce a perfectly reasonable but unsafe action.

Example:

```text
11:04  observe deployment health = healthy
11:05  deployment rolls forward
11:06  model proposes rollback using 11:04 evidence
```

The loop should know that the evidence is stale and reacquire it before a high-impact action.

## 6.2 Observation quality gates

A loop may reject an observation when:

- it is outside its freshness window;
- its source is unavailable or degraded;
- tenant/resource scope does not match;
- required fields are missing;
- the source is not authoritative for the decision.

---

# 7. Decision engineering

The model should return a **proposal**, not an uncontrolled side effect.

Example typed proposal:

```json
{
  "action": "query_siem",
  "arguments": {
    "user_id": "u-17",
    "window_minutes": 30
  },
  "reason": "Need corroborating login events",
  "expected_observation": "Recent authentication events"
}
```

The loop then checks:

1. Is the action known?
2. Are the arguments valid?
3. Is the resource in scope?
4. Is the tenant correct?
5. Is the action authorized?
6. Is approval required?
7. Does the action fit the remaining budget?
8. Is the action idempotent or safely repeatable?

An invalid proposal terminates or returns to decision repair; it does not silently become executable code.

---

# 8. Policy and authority boundaries

The model must not be able to rewrite the rules governing the loop.

Treat these as control-plane state:

```text
identity
tenant
permissions
policy version
approval status
budget
deadline
kill-switch status
```

Treat these as data-plane inputs:

```text
user text
retrieved documents
memory snippets
web content
emails
tickets
tool messages
```

### Precedence

A useful default is:

```text
Security deny
    ↓
Governance / legal restriction
    ↓
Tenant / resource authorization
    ↓
Workflow approval
    ↓
Task preferences
    ↓
Model proposal
```

The organization may implement a different hierarchy, but it must be explicit and testable.

---

# 9. Action engineering and side-effect safety

A loop becomes dangerous at the moment it leaves read-only reasoning and causes an external effect.

Every side effect should have an action identity, for example:

```text
action_id = hash(
    task_id,
    action_type,
    target_resource,
    canonical_arguments,
    action_version
)
```

Use that identity to support:

- idempotent writes;
- duplicate-delivery detection;
- audit correlation;
- recovery after worker crashes;
- reconciliation when outcome is unknown.

### Unknown outcome is not failure

This is a critical production distinction:

```text
request sent
    ↓
network timeout
    ↓
Did the side effect happen?
```

The answer may be unknown.

Blindly retrying can create duplicates. Instead:

```text
TIMEOUT / UNKNOWN
        ↓
RECONCILE external state
        ├── already applied → record success
        ├── not applied      → retry safely
        └── cannot determine  → escalate / hold
```

---

# 10. Verification engineering

A model statement such as:

```text
"Rollback completed successfully."
```

is not verification.

Verification should check an independent postcondition.

### Examples

| Domain | Action | Independent postcondition |
|---|---|---|
| SRE | Roll back deployment | error rate and deployed version match target |
| SOC | Disable account | IAM reports disabled state |
| Coding | Apply patch | tests pass and diff is within allowed scope |
| Banking | Reconcile transaction | independent ledger totals reconcile |
| Support | Issue refund | payment ledger shows exact refund |

### Verification levels

```text
L0: model self-report
L1: same-source confirmation
L2: independent query
L3: independent verifier / invariant
L4: human confirmation for high-risk outcome
```

Use stronger verification where the consequence of error is higher.

---

# 11. Recovery and retry taxonomy

Do not implement a single `retry=True` switch.

| Failure | Default response |
|---|---|
| transient timeout | bounded retry |
| rate limit | backoff / retry within deadline |
| malformed proposal | repair once / reject |
| authorization denial | stop; do not retry blindly |
| policy denial | stop / escalate |
| deterministic validation error | correct input or stop |
| dependency outage | circuit break / safe stop |
| stale observation | reacquire evidence |
| unknown side effect | reconcile before retry |
| repeated verifier failure | escalate |
| corrupted checkpoint | reject / recover from earlier safe point |

### Retry budget

Track both **attempt count** and **amplification**:

```text
logical action = 1
network attempts = 4
provider failures = 3
```

This makes outage-driven load amplification visible.

---

# 12. Progress and loop pathologies

A system may keep taking actions without getting closer to its goal.

Detect at least:

### Infinite repetition

```text
A → B → A → B → A → B ...
```

### No-progress loop

```text
observe
query same evidence
observe identical evidence
query same evidence
```

### Tool ping-pong

```text
search → summarize → search → summarize → ...
```

### Oscillating plan

```text
plan X
plan Y
plan X
plan Y
```

### Churn without evidence gain

Repeated model calls that change wording but not world state.

### Guard patterns

Use multiple independent brakes:

```text
max steps
max repeated state
max repeated action
max model calls
max tool calls
max time
max money
minimum progress requirement
kill switch
human escalation
```

Hard budgets are necessary but not sufficient. A loop may terminate within budget and still be unsafe, so **progress and verification** must also be first-class signals.

---

# 13. Budgets, deadlines, and cancellation

A loop should know when it must stop before it starts.

Recommended budget dimensions:

```text
wall_clock
model_calls
tool_calls
retrieval_calls
input_tokens
output_tokens
estimated_cost
high_risk_actions
parallelism
```

### Deadline propagation

A deadline should travel with the task:

```text
Task deadline = 18:00
      ↓
model call must finish before deadline
      ↓
tool timeout must fit remaining time
      ↓
retry budget shrinks as deadline approaches
```

### Cancellation

Cancellation should be a control event, not a prompt such as “please stop.”

Safe cancellation means:

1. reject new work;
2. cancel interruptible in-flight work;
3. prevent new side effects;
4. record the cancellation cause;
5. persist enough state to resume safely when allowed.

---

# 14. Checkpoints and recovery boundaries

Checkpointing exists to preserve **semantic recovery**, not merely a loop counter.

A useful checkpoint can contain:

```text
task_id
state_version
current_phase
last_successful_observation
approved_action_id
completed_side_effect_ids
verification_result
budget_remaining
deadline
policy_version
trajectory_position
```

### Boundary rule

Checkpoint especially:

- after important observations;
- before high-impact side effects;
- after committed side effects;
- after independent verification;
- before a long-running wait.

For a side effect:

```text
prepare
  ↓
checkpoint
  ↓
execute with action_id
  ↓
reconcile / verify
  ↓
checkpoint committed outcome
```

Module 38 will extend this into long-running durable execution; Module 36 teaches the recovery semantics that make such persistence meaningful.

---

# 15. Trajectory and replay

A useful trajectory is not just a log line per model call. It is a structured history of the control loop.

Minimum fields:

```text
run_id
task_id
tenant_id
state_version
phase
observation_ref
proposal
policy_decision
action_id
tool_result_ref
verification_result
error_class
latency
tokens
cost
stop_reason
```

A replay should be able to answer:

> What did the system know, what did it propose, what did the policy permit, what actually happened, and why did it continue or stop?

Replay need not reproduce every probabilistic model token. It should reproduce the **decision-relevant trajectory and externally observed effects**.

---

# 16. Failure-first engineering

Treat failures as part of the curriculum, not as an afterthought.

Inject at least:

```text
provider outage
stale observation
tool timeout
rate limit
duplicate delivery
malformed action
policy denial
authorization denial
budget exhaustion
deadline expiry
false verification
worker crash
corrupted checkpoint
prompt injection
poisoned tool output
unknown side effect
```

For every fixture record:

```text
Detection signal
Containment boundary
Retry / recover / stop decision
Expected user-visible result
Residual risk
Evidence captured
Regression test
```

---

# 17. Comparative architectures

Use the same workload to compare:

### Fixed workflow

```text
Step 1 → Step 2 → Step 3 → Step 4
```

Strength: predictable cost and behavior.  
Weakness: poor adaptation to unexpected states.

### Reactive single-agent loop

```text
Observe → Decide → Act → Observe → ...
```

Strength: adaptable.  
Weakness: can become expensive, unstable, or hard to govern.

### Guarded adaptive loop

```text
Observe → Decide → Policy → Act → Verify
        ↑             ↓          ↓
        └──── Recovery / Budget / Stop
```

Strength: adaptation with explicit control boundaries.  
Weakness: more engineering and more state to test.

Measure all three rather than assuming the most autonomous design is best.

---

# 18. Industry labs

## Lab 1 — SOC investigation loop

Investigate suspicious login activity. Permit read-only enrichment autonomously; require explicit approval before containment.

**Break:** malicious alert text attempts to redefine policy.  
**Measure:** investigation completion, false containment, time-to-decision, tool calls.

## Lab 2 — SRE remediation loop

Detect elevated 5xx rate, identify deployment, propose rollback, obtain approval, execute, and independently verify service health.

**Break:** stale metric snapshot.  
**Measure:** recovery time, false rollback rate, verification latency.

## Lab 3 — Coding-agent repair loop

Inspect failing tests → propose patch → apply scoped change → run tests → inspect diff → verify → stop or iterate.

**Break:** patch tries to modify files outside repository scope.  
**Measure:** first-pass fix rate, regressions, patch attempts, diff size.

## Lab 4 — Banking reconciliation

Read ledger and settlement records, locate mismatch, propose correction, gate monetary correction, and verify against an independent ledger invariant.

**Break:** write call times out after possible settlement.  
**Measure:** duplicate-prevention rate, reconciliation accuracy, escalation rate.

## Lab 5 — Typed proposal boundary

Create valid and invalid action proposals. Reject unknown tools, malformed arguments, wrong tenant, out-of-scope targets, missing approval, and over-budget actions.

**Deliverable:** acceptance/rejection matrix.

## Lab 6 — Retry and idempotency

Simulate flaky dependencies with transient, permanent, authorization, timeout, and unknown-outcome failures.

**Gold property:** no duplicate external side effect.

## Lab 7 — Independent verification

Implement independent postconditions for service health, repository tests, and financial reconciliation.

**Break:** model reports success while the external world remains incorrect.

## Lab 8 — Halting and pathology detection

Build infinite-loop, oscillation, repeated-state, and tool-ping-pong fixtures.

**Gold property:** every fixture ends in success, safe failure, or human escalation.

## Lab 9 — Crash recovery

Crash at observation, pre-side-effect, post-side-effect, and post-verification boundaries.

**Deliverable:** recovery state table + duplicate-side-effect proof.

## Lab 10 — Security boundary

Inject prompt injection, poisoned retrieval, hostile memory, and malicious tool messages.

**Gold property:** untrusted data cannot rewrite policy, tenant, identity, budget, or approvals.

## Lab 11 — Loop economics

Compare cost per successful task across fixed, reactive, and guarded adaptive loops.

Track retry amplification and human escalation cost.

## Lab 12 — Replayable trajectory

Generate an incident timeline from structured loop events and explain every continuation/stop decision.

## Lab 13 — Concurrency and ordering

Add two safe parallel reads and one ordering-sensitive write.

**Break:** stale branch result arrives after a newer state version.  
**Measure:** valid commit rate and conflict handling.

## Lab 14 — Production architecture review

Design the loop as a deterministic execution kernel surrounded by model proposals, policy checks, tool gateways, durable state, verifiers, and telemetry.

## Lab 15 — Failure-injection day

Run the complete matrix above. No happy-path-only grading is accepted.

---

# 19. Measurement framework

Evaluate loops across several dimensions rather than one “accuracy” score.

| Dimension | Example metric |
|---|---|
| Task quality | successful task rate |
| Safety | policy violation rate / false containment |
| Progress | useful state transitions / iteration |
| Reliability | recovery rate |
| Verification | verifier agreement / false-success rate |
| Efficiency | tool calls / successful task |
| Latency | p50 / p95 completion |
| Cost | cost / successful task |
| Autonomy | human escalation rate |
| Stability | repeated-state / oscillation rate |
| Auditability | replay completeness |

### Core scorecard

```text
Quality + Safety + Reliability + Efficiency + Auditability
```

A system that is cheaper but causes unsafe side effects is not an improvement.

---

# 20. System-design challenge

### Autonomous SOC investigator — 10,000 alerts/day

Design a loop that can:

- triage alerts;
- gather identity/network evidence;
- distinguish read-only from high-risk actions;
- require approval for containment;
- recover from tool/provider failures;
- prevent duplicate actions;
- terminate pathological loops;
- preserve tenant isolation;
- produce replayable evidence;
- measure quality, safety, cost, and latency.

Defend:

1. state machine;
2. observation freshness;
3. proposal schema;
4. policy boundary;
5. action identity;
6. verification strategy;
7. retry taxonomy;
8. budget/deadline model;
9. checkpoint boundaries;
10. concurrency model;
11. stop/escalation conditions;
12. evaluation plan.

---

# 21. Loop Contract delivered to Module 37

At the end of Module 36, produce a concrete artifact called **Loop Contract v1** containing:

```text
1. State model
2. Transition table
3. Action schema
4. Policy insertion points
5. Verification/postcondition definitions
6. Retry taxonomy
7. Idempotency / action identity strategy
8. Budget and deadline rules
9. Stop and escalation rules
10. Checkpoint boundaries
11. Trajectory schema
12. Failure matrix
13. Benchmark fixtures
```

Module 37 then turns that contract into a reusable **agent harness** with context management, state storage, tool/capability gateways, policy infrastructure, checkpoint/replay services, and operational controls.

This separation prevents the course from teaching the same thing twice:

```text
Module 36 = engineer the loop
Module 37 = engineer the reusable harness around the loop
Module 38 = engineer durable long-running execution
Module 39 = engineer skills, memory, and continual harnesses
```

---

# 22. Mastery gate

A learner passes when they can demonstrate, not merely describe:

- explicit state transitions;
- typed model proposals;
- policy isolation;
- bounded execution;
- progress detection;
- correct failure classification;
- safe retries and idempotency;
- independent verification;
- safe cancellation and deadlines;
- checkpoint/recovery semantics;
- replayable trajectories;
- failure-injection coverage;
- measured quality/cost/safety trade-offs.

### Gold standard

> Given a malicious proposal, stale observation, transient failure, unknown side effect, false verifier, worker crash, and exhausted budget, the loop must still terminate in a defensible state without losing control of authorization, tenant scope, safety policy, or auditability.

---

## 23. Framework rule

Implement the mechanism first. Then map it to one or more frameworks.

A framework is useful when it reduces implementation cost **without hiding the loop semantics**.

The learner should be able to explain the underlying transition, invariant, failure mode, and verification contract even when the framework is removed.

---

## 24. Repository practice

The canonical implementation is:

- `36-loop-engineering/README.md`
- `36-loop-engineering/notebooks/module_36_loop_engineering.ipynb`
- `36-loop-engineering/app/`
- `36-loop-engineering/exercises/`
- `36-loop-engineering/tests/`

Keep Module 36 focused on the loop. Reusable runtime infrastructure belongs in Module 37; long-running durability belongs in Module 38. Do not recreate legacy duplicate module directories.
