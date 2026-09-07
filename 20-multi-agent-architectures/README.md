# Module 20 — Multi-Agent Architectures: Supervisor / Worker Systems

## Mission

Turn the architectural decision from Module 19 into an engineered multi-agent runtime. Build a supervisor/worker system with explicit contracts, bounded delegation, capability isolation, deadlines, retries, partial-failure recovery, verification and observability.

**Core principle:** orchestration is software engineering. The supervisor may choose *which* authorized worker to invoke, but it must not invent permissions, bypass policy or silently redefine contracts.

## Learning outcomes

You will learn to:
- model supervisor, worker, aggregator and verifier roles;
- represent tasks as typed envelopes;
- route work using deterministic constraints plus model judgment;
- enforce per-worker capabilities and budgets;
- support fan-out/fan-in and sequential dependencies;
- recover failed workers without duplicating completed work;
- handle worker disagreement explicitly;
- prevent recursive delegation and orchestration loops;
- observe the entire agent graph;
- compare supervisor architectures with queues and workflows.

## 1. Reference architecture

```text
                         +----------------+
                         | Task Contract  |
                         +-------+--------+
                                 v
                       +---------+----------+
                       | Supervisor Agent   |
                       | plan / route       |
                       +----+----+----+-----+
                            |    |    |
                    +-------+    |    +-------+
                    v            v            v
                +-------+    +-------+    +-------+
                |Research|    |Finance|    |Technical|
                |Worker |    |Worker |    |Worker   |
                +---+---+    +---+---+    +----+----+
                    \            |            /
                     +-----------+-----------+
                                 v
                         +-------+--------+
                         | Aggregator     |
                         +-------+--------+
                                 v
                         +-------+--------+
                         | Independent    |
                         | Verifier       |
                         +----------------+
```

The security boundary from Module 18 wraps every worker and tool.

## 2. Worker contract

A worker receives:

- task ID;
- parent run ID;
- tenant ID;
- authorized capability set;
- input schema;
- output schema;
- deadline;
- token/tool/cost budget;
- retry policy;
- verification criteria;
- cancellation signal.

A worker must never infer authority from free-form supervisor text.

## 3. Supervisor responsibilities

The supervisor should:

1. validate the task contract;
2. decompose work;
3. select eligible workers;
4. allocate bounded budgets;
5. issue explicit task envelopes;
6. collect structured results;
7. retry only safe/idempotent operations;
8. cancel obsolete branches;
9. escalate unresolved conflicts;
10. submit the final result for verification.

## 4. Worker responsibilities

A worker should:

- stay within its capability boundary;
- validate input;
- execute only its assigned task;
- return structured evidence;
- report uncertainty and failure;
- emit telemetry;
- avoid hidden side effects;
- honor cancellation and deadline propagation.

## 5. Routing strategies

### Rule-first routing
Deterministic metadata selects candidates, then an LLM chooses among them.

### Capability-first routing
Filter workers by capability before model selection.

### Cost-aware routing
Choose the cheapest eligible worker meeting the required quality class.

### Reliability-aware routing
Prefer workers with historical success for the relevant task slice.

### Hybrid routing
`constraints → candidate set → model selection → policy check → execution`

Never reverse this into `model chooses anything → security checks later`.

## 6. Fan-out / fan-in

For independent subtasks:

`Supervisor → {W1,W2,W3} → Aggregator`

Benefits:
- lower wall-clock latency;
- specialist context;
- failure isolation.

Costs:
- duplicated retrieval;
- more tokens;
- more coordination;
- inconsistent evidence;
- aggregator complexity.

Use bounded concurrency and a global deadline.

## 7. Sequential delegation

Some tasks require dependencies:

`Research → Analysis → Recommendation → Verification`

Represent dependencies explicitly rather than letting the supervisor improvise hidden state.

## 8. Partial failure

A production system must distinguish:

- worker failed before execution;
- worker timed out;
- worker returned invalid output;
- worker completed but verifier rejected result;
- worker completed and result is durable.

Only retry when the failure mode and action semantics permit it.

## 9. Disagreement handling

Do not average incompatible answers blindly.

Return structured disagreement:

```text
claim
supporting evidence
worker confidence
contradicting evidence
missing information
recommended next action
```

Then use an independent verifier or escalation path.

## 10. Detailed labs

### Lab 1 — Typed task envelopes
Implement task IDs, parent IDs, tenant, worker type, capabilities, budgets and deadlines.

### Lab 2 — Supervisor router
Build deterministic candidate filtering followed by a simple model-like selection function.

### Lab 3 — Fan-out/fan-in
Run three workers concurrently with bounded concurrency and collect structured outputs.

### Lab 4 — Worker crash
Crash one worker and recover only that branch from durable state.

### Lab 5 — Duplicate delivery
Deliver the same task twice. Use idempotency keys to prevent duplicate side effects.

### Lab 6 — Deadline propagation
Give the whole run 5 seconds. Propagate the remaining deadline to every worker.

### Lab 7 — Capability escalation
Attempt to make the research worker call a finance capability. Prove denial occurs outside the model.

### Lab 8 — Recursive supervisor
Allow a worker to request another worker. Add delegation depth and total-call limits.

### Lab 9 — Conflicting evidence
Make two workers return contradictory evidence. Require an independent verifier to resolve or escalate.

### Lab 10 — Cost-aware routing
Give workers different cost and reliability profiles. Route using a constrained optimization heuristic.

### Lab 11 — Queue-based orchestration
Replace direct calls with a task queue abstraction. Compare durability and latency.

### Lab 12 — Production trace
Create a graph trace reconstructing supervisor decisions, worker tasks, tool calls, outputs and verification.

## 11. Failure injection

Break deliberately:

1. supervisor assigns unauthorized capability;
2. worker output schema is malformed;
3. worker is duplicated;
4. worker never terminates;
5. supervisor recursively delegates forever;
6. aggregator accepts unsupported claims;
7. cancellation arrives after task assignment;
8. worker retries a non-idempotent action;
9. tenant ID is changed in a child envelope;
10. verifier receives the same poisoned context as workers.

For each: **failure → blast radius → detection → containment → regression test**.

## 12. Production controls

- capability allowlists;
- per-worker and global budgets;
- deadline propagation;
- idempotency;
- durable checkpoints;
- cancellation;
- structured outputs;
- schema validation;
- independent verification;
- security policy at every tool boundary;
- correlation IDs;
- audit logs;
- dead-letter handling.

## 13. Observability

Minimum trace:

`run → supervisor decision → worker task → tool call → result → aggregation → verification`

Measure:
- worker success rate;
- routing accuracy;
- queue/wait time;
- execution time;
- tokens and cost per worker;
- retries;
- duplicate work;
- disagreement rate;
- verification rejection rate;
- end-to-end success.

## 14. Industry scenarios

**Banking:** supervisor can delegate evidence gathering, but payment execution remains a separate capability boundary.

**Healthcare:** document specialists may work in parallel while patient-resource authorization and final verification remain centralized.

**Cybersecurity:** reconnaissance workers can parallelize; containment workers require stricter capabilities and approvals.

**Enterprise IT:** diagnostics can fan out across systems; production mutation should remain policy-gated.

## 15. Interview questions

1. What belongs in a worker contract?
2. How do you prevent a supervisor from escalating privileges?
3. How do you propagate deadlines?
4. When can a failed worker safely retry?
5. How do you guarantee exactly-once side effects?
6. How do you handle contradictory workers?
7. Why is a queue useful?
8. How do you cap recursive delegation?
9. How would you debug a supervisor routing error?
10. What metrics prove a multi-agent system is helping?
11. How do you isolate tenant state?
12. How would you implement cancellation?
13. What should the aggregator never infer?
14. Why does an independent verifier matter?
15. How would you migrate from direct calls to durable queues?

## 16. System-design challenge

Design a multi-agent enterprise operations platform with research, analytics, security and execution workers. Requirements: multi-tenancy, 99.9% availability, bounded cost, human approval for production mutation, restart recovery and complete auditability.

## 17. Coding challenges

- Task envelope validator
- Worker registry
- Capability-aware router
- Bounded fan-out executor
- Deadline propagation
- Idempotent task dispatcher
- Partial-failure recovery
- Conflict resolver
- Delegation-depth guard
- Graph trace exporter

## 18. Mastery gate

You pass when you can build and defend a supervisor/worker system that:

- survives worker failure;
- rejects malformed results;
- prevents capability escalation;
- respects deadlines and budgets;
- avoids duplicate side effects;
- handles disagreement explicitly;
- produces a complete trace;
- demonstrates measurable value over the Module 19 baseline.

## Gold challenge

Build **AegisAI Supervisor/Worker Runtime** with durable task envelopes, capability-scoped workers, bounded fan-out/fan-in, retries, cancellation, partial-failure recovery, independent verification and a graph-level audit trail.
