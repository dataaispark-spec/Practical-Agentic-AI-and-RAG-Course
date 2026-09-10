# Module 36 — Loop Engineering

**Canonical implementation:** `36-loop-engineering/`. Former `31-loop-engineering/` is legacy only.

## Mission
Build the **deterministic execution kernel** beneath an agent. Module 14 teaches the raw loop; Module 36 teaches the engineering semantics that make repeated autonomous execution bounded, authorized, verifiable, recoverable and auditable; Module 37 then packages those semantics into a reusable harness.

## Why this module exists
An LLM can propose an action, but it must not own authority, budgets, tenant identity, side-effect semantics or the truth of completion. Loop Engineering puts deterministic control around probabilistic decisions:

`TASK → OBSERVE → DECIDE/PROPOSE → POLICY → ACT → VERIFY → RECOVER → CONTINUE/STOP`

The full theory and component deep dive is in [`theory/LOOP-ENGINEERING-THEORY.md`](theory/LOOP-ENGINEERING-THEORY.md).

## Learning outcomes
You will be able to:
- model an agent loop as an explicit state machine;
- separate the control plane from untrusted data-plane inputs;
- design observation freshness/provenance contracts;
- constrain model output to typed proposals;
- enforce identity, tenant, risk, approval and budget policy outside the model;
- design an action gateway with stable action identity and idempotency;
- define independent postconditions and verification levels;
- classify failures into retry, reobserve, reconcile, recover, stop or escalate;
- detect infinite loops, oscillation, plan churn and retry storms;
- engineer budgets, deadlines, cancellation and kill switches;
- checkpoint semantic state and recover after crashes;
- prevent stale concurrent branches from overwriting authoritative state;
- create replayable trajectories and meaningful production metrics.

## Core architecture
```text
                         TASK CONTRACT
                              │
                              ▼
                       ┌────────────┐
                       │   OBSERVE  │◄──────────────┐
                       └─────┬──────┘               │
                             ▼ evidence              │
                       ┌────────────┐               │
                       │   DECIDE   │               │
                       │ / PROPOSE  │               │
                       └─────┬──────┘               │
                             ▼ typed proposal       │
                       ┌────────────┐               │
                       │   POLICY   │               │
                       └─────┬──────┘               │
                             ▼ allowed              │
                       ┌────────────┐               │
                       │    ACT     │──────────┐    │
                       └─────┬──────┘          │    │
                             ▼ effect          │    │
                       ┌────────────┐          │    │
                       │   VERIFY   │          │    │
                       └─────┬──────┘          │    │
                         ┌───┴────┐             │    │
                    success      failure       │    │
                       ▼            ▼           │    │
                   COMPLETE      RECOVER ──────┘    │
                                    │                │
                         REOBSERVE / REPLAN / STOP  │
                                                     │
       CONTROL PLANE: identity • tenant • policy • approval
       budget • deadline • concurrency • checkpoint • audit
       idempotency • cancellation • kill switch • evaluation
```

## Component deep dive

| Component | Architectural responsibility | Key failure it prevents |
|---|---|---|
| Task contract | objective, scope, limits | undefined work / runaway execution |
| Observation | fresh, scoped evidence | stale-state decisions |
| Decision/proposal | model reasoning → typed action | free-form unsafe actions |
| Policy gate | authority, tenant, risk, approval, budget | privilege/policy bypass |
| Action gateway | validation, identity, idempotency, timeout | duplicate/unsafe side effects |
| Verification | independent postcondition | false completion |
| Recovery controller | explicit failure disposition | blind retries |
| State/versioning | authoritative execution state | stale commits |
| Budget/deadline | hard resource limits | cost/time runaway |
| Checkpoint | durable semantic state | crash-induced loss/duplication |
| Trace/audit | decision trajectory | unexplainable execution |
| Cancellation | controlled stop | side effects after cancellation |
| Termination | complete/stop/escalate semantics | infinite loops |

### State-machine contract

| Transition | Required condition | Failure response |
|---|---|---|
| START → OBSERVE | valid task contract | reject |
| OBSERVE → DECIDE | fresh/in-scope evidence | reobserve/escalate |
| DECIDE → POLICY | typed proposal | repair/reject |
| POLICY → ACT | authorization + budget + approval | deny/escalate |
| ACT → VERIFY | attempt recorded | reconcile if unknown |
| VERIFY → COMPLETE | independent postcondition | complete |
| VERIFY → RECOVER | false/unknown postcondition | recover/replan |
| RECOVER → OBSERVE | new evidence required | observe |
| RECOVER → STOP | unsafe/unrecoverable | safe stop |

## Deep engineering topics

### Observation freshness
Capture source, timestamp/freshness, provenance, scope and state version. Stale evidence is a control problem, not merely a data-quality warning.

### Policy boundary
The model may propose `disable_account(tenant=b)`; the policy layer must reject it if the authoritative task tenant is `a`. Retrieved text, memory and tool output cannot rewrite this boundary.

### Side-effect semantics
`write → timeout` is **UNKNOWN**, not necessarily failure. Reconcile external state using stable action identity before retrying.

### Verification hierarchy
`model claim → same-source confirmation → independent query → deterministic invariant/verifier → human confirmation`.

Verification strength must scale with action risk.

### Retry taxonomy
Timeout/rate-limit may be retryable; malformed arguments may require repair; authorization denial should stop/escalate; stale evidence should reobserve; unknown side effects should reconcile; exhausted budgets should safe-stop.

### Loop pathologies
Teach and test infinite loops, A↔B oscillation, plan churn, repeated observations, retry storms and no-progress execution. Hard budgets remain mandatory even when progress heuristics exist.

### Persistence and concurrency
Checkpoint semantic state around side effects. Use state versions, leases or serialization so an old branch cannot overwrite newer authoritative state.

## Labs
1. SOC investigation loop.
2. SRE rollback loop with approval.
3. Coding-agent repair loop.
4. Banking reconciliation with independent verification.
5. Typed model proposals and invalid-action rejection.
6. Retry/timeout/idempotency taxonomy.
7. Independent postconditions.
8. Infinite-loop and no-progress detection.
9. Crash recovery around side effects.
10. Prompt-injection/security boundary.
11. Cost per successful iteration.
12. Replayable trajectory telemetry.
13. Fixed vs reactive vs guarded adaptive benchmark.
14. Production architecture review.
15. Failure-injection day.

## Failure contract
Inject provider outage, stale observation, tool timeout, duplicate delivery, malformed action, budget exhaustion, authorization denial, false verification, worker crash and corrupted checkpoint. For every failure record **detection → evidence → containment → retry/recover/stop decision → regression test → residual risk**.

## Measures
Verified task success, unsafe-action acceptance, verifier failure rate, recovery rate, escalation rate, iterations/success, tool calls/success, model calls/success, p50/p95/p99 latency, cost/success, retry rate, unknown-side-effect rate and loop-pathology rate.

## Exercises / system design
Design an autonomous SOC investigator for **10,000 alerts/day**. Defend termination, observation freshness, typed proposals, identity/tenant boundaries, approval gates, idempotency, independent verification, concurrency, checkpointing, replay, cost controls and auditability.

## Security
User input, retrieved documents, memory and tool outputs are untrusted data. None may redefine identity, tenant, policy, budget, approval requirements or termination rules. High-impact approvals should bind to the exact action identity and canonical arguments.

## GitHub deliverables
- `theory/LOOP-ENGINEERING-THEORY.md` — chapter-level theory and component deep dive
- `app/loop_engine.py` — deterministic reference execution kernel
- `notebooks/module_36_loop_engineering.ipynb` — executable failure-first lab
- `tests/` — regression tests for loop semantics
- failure matrix + benchmark evidence
- state/transition design and production ADR

## Mastery gate
A student must draw and explain the complete state machine, identify every control boundary, implement the loop without an agent framework, inject failures, prove idempotency and independent verification, measure cost/latency/safety trade-offs, and defend why the selected loop strategy is appropriate.

**Handoff:** Module 36 engineers the loop semantics. Module 37 engineers the reusable harness around those semantics. Module 38 engineers durable execution across crashes and long horizons.
