# Module 16 — Stateful Agent Workflows & LangGraph

## Mission
Move from a raw agent loop to explicit graph orchestration. The learner should understand **why** graph state, nodes, edges, checkpoints and interrupts exist before relying on a framework abstraction.

## Core architecture
```text
                 ┌──────────────┐
                 │ Shared State │
                 └──────┬───────┘
                        ▼
                 [Observe Node]
                        │
                        ▼
                 [Decision Node]
                  /     |      \
             tool     verify    human
              |         |         |
              ▼         ▼         ▼
          [Tool] → [Verifier] → [Approval]
              \         |         /
               └────► [Router]
                         │
                 ┌───────┴───────┐
                 ▼               ▼
              Continue          END
```

## Why a graph?
A raw loop is excellent for understanding mechanics. A graph becomes useful when the workflow has explicit states, branching, retries, human interrupts, durable checkpoints and inspectable transitions.

Use a graph when the control flow itself is important. Do not use one merely because an agent library offers it.

## Learning outcomes
Build and reason about:
- typed shared state;
- nodes and deterministic transitions;
- conditional routing;
- retries and error edges;
- checkpoints;
- durable execution;
- interrupts/resume;
- human-in-the-loop approval;
- subgraphs;
- state reducers;
- replay/time-travel debugging;
- idempotent nodes;
- graph-level observability;
- graph security.

## State design
A graph state should distinguish:
- user goal;
- task status;
- evidence;
- messages/context;
- tool outputs;
- pending approval;
- retry counters;
- budget;
- provenance;
- final result.

Avoid uncontrolled mutable global state. Define which node owns each field and how concurrent updates are merged.

## Node contract
A node should be a bounded unit of work:

`State → NodeResult → StateUpdate | Error`

Keep side effects behind explicit tool/service boundaries. Make pure decision nodes easy to test.

## Edge types
1. **Sequential:** A → B.
2. **Conditional:** A → B/C based on state.
3. **Retry:** failure → bounded retry.
4. **Fallback:** failure → alternate strategy.
5. **Human interrupt:** workflow → approval → resume.
6. **Terminal:** → END.

## Checkpointing
Checkpoint at meaningful boundaries, especially before/after external side effects and before human approval. A checkpoint should make the run recoverable without repeating non-idempotent work.

## Human-in-the-loop
Approval is a graph state, not a prompt trick:

```text
propose action
   ↓
validate policy
   ↓
WAITING_FOR_APPROVAL
   ↓
approved? ── no ──→ reject/end
   │
  yes
   ↓
execute
   ↓
verify
```

The human decision must be durable, attributable and bound to the exact action being approved.

## Lab 1 — Graph from raw loop
Translate Module 14's loop into explicit nodes and edges. Compare trace readability.

## Lab 2 — Conditional routing
Route requests into answer, retrieval, tool-action or escalation paths.

## Lab 3 — Checkpoint/restart
Pause after a tool call, restart the process and resume from the checkpoint without duplicating the side effect.

## Lab 4 — Human approval
Create a high-impact action node that cannot execute until an approval record exists.

## Lab 5 — Retry/fallback
Distinguish transient tool errors from semantic failures and route them differently.

## Lab 6 — Subgraphs
Create a reusable research subgraph and invoke it from multiple parent workflows.

## Lab 7 — State reducers
Run parallel branches that return partial evidence and deterministically merge their updates.

## Lab 8 — Replay/time travel
Persist state snapshots and reproduce a bad decision from the exact prior state.

## Lab 9 — Graph security
Attempt to bypass approval by jumping directly to an action node. Enforce policy at the action boundary.

## Lab 10 — Production workflow
Build an enterprise support agent: classify → retrieve → diagnose → propose remediation → approve → execute → verify → close.

## Detailed exercises
1. Define a typed graph state.
2. Implement node contracts.
3. Implement deterministic routers.
4. Add conditional edges.
5. Add retry edges.
6. Add fallback edges.
7. Add terminal states.
8. Add durable checkpoints.
9. Add approval interrupts.
10. Bind approval to an action hash.
11. Add idempotency keys.
12. Add state versioning.
13. Implement state reducers.
14. Add parallel branches.
15. Add graph tracing.
16. Add replay.
17. Add cancellation.
18. Add timeout/deadline propagation.
19. Add graph-level budget enforcement.
20. Compare raw-loop and graph implementations.

## Failure-first labs
### Skipped approval
Try to invoke execution without approval. It must fail closed.

### Duplicate side effect
Replay after a crash. The same payment/change/ticket update must not happen twice.

### Lost state
Kill the process between nodes. Resume from a durable checkpoint.

### Bad router
Force an ambiguous classification. Verify the graph escalates instead of choosing an unsafe branch.

### Reducer conflict
Two parallel nodes update the same field differently. Detect or deterministically resolve the conflict.

### Infinite graph cycle
Create A → B → A. Prove bounded traversal/iteration terminates.

### Stale approval
Change the action after approval. The original approval must not authorize the modified action.

## Production metrics
Track:
- node latency;
- edge-transition counts;
- graph completion rate;
- retries;
- checkpoint/recovery rate;
- human approval latency;
- approval rejection rate;
- duplicate-side-effect prevention;
- state conflicts;
- p95/p99 workflow latency;
- cost per completed workflow.

## Framework principle
LangGraph is introduced as an orchestration tool, not as the underlying concept. Students should be able to explain and implement the equivalent state-machine behavior using ordinary Python before using framework APIs.

## Industry scenarios
**Banking:** loan/document workflow with approval gates and durable state.

**Healthcare:** clinical research workflow with evidence provenance and mandatory review before high-impact recommendations.

**Cybersecurity:** alert triage → evidence collection → correlation → analyst approval → response.

**Enterprise IT:** incident diagnosis → remediation proposal → change approval → execution → verification.

## Interview bank
1. Why use a graph instead of a while loop?
2. What is graph state?
3. How do conditional edges work?
4. How do you make nodes idempotent?
5. Where should checkpoints occur?
6. How do you safely resume after a crash?
7. How do you prevent approval bypass?
8. What is time-travel debugging?
9. How do parallel state updates create conflicts?
10. How would you version graph state?
11. How do retries differ from graph transitions?
12. When is a graph overengineering?
13. How would you test every branch?
14. How do you propagate budgets across nodes?
15. How would you migrate a live graph workflow?

## System-design challenge
Design a durable graph runtime for 50,000 concurrent workflows with checkpointing, human interrupts, idempotent side effects, conditional routing, replay, observability and tenant isolation.

## Mastery gate
Build a stateful support workflow that survives process restart, pauses for approval, prevents duplicate actions, recovers transient failures and produces a complete replayable trace.

## Gold challenge
Implement the same workflow once as a raw state machine and once with LangGraph. Benchmark developer complexity, execution latency, recovery behavior, observability, testability and operational risk. Defend where the framework adds genuine value.

## Google Colab
`notebooks/module_16_langgraph_stateful_workflows.ipynb` provides a progressive executable lab. The first half implements graph mechanics without dependencies; later cells can be extended with LangGraph in an environment where the package is installed.
