# Module 22 — Multi-Agent Debugging: Distributed Agent Debugging Lab

## Mission

Debug multi-agent systems as distributed systems with probabilistic decision points. The objective is to move from **"the answer is wrong"** to a reproducible causal explanation:

`wrong outcome → verifier failure → aggregator input → worker result → tool/retrieval evidence → policy/state/message transition`

## Learning outcomes

You will learn to:

1. Define a trace contract for every agent run.
2. Correlate parent/child tasks, messages, tools and state transitions.
3. Identify the first causal failure rather than the last visible symptom.
4. Separate model errors from retrieval, tool, policy, orchestration and state errors.
5. Replay a failed trajectory deterministically where possible.
6. Compare expected vs actual agent decisions.
7. Debug latency and cost regressions.
8. Investigate security incidents across agent boundaries.
9. Create regression tests from production failures.
10. Produce an incident report that another engineer can reproduce.

## 1. Debugging mental model

A final answer is an output, not a root cause.

Example:

```text
Final answer wrong
   ↓
Verifier rejected citation
   ↓
Aggregator received unsupported claim
   ↓
Research worker selected wrong document
   ↓
Retriever returned stale chunk
   ↓
Index version mismatch
```

Fixing the final prompt would treat the symptom, not the cause.

## 2. Trace contract

Every meaningful event should contain:

```text
run_id
parent_run_id
agent_id
message_id
causation_id
timestamp
state_version
model/provider/version
prompt/template version
tool/version
retrieval/index version
input/output hashes
latency
tokens/cost
policy decision
security classification
error/retry metadata
```

Do not log secrets or unrestricted sensitive content merely for debugging.

## 3. Event taxonomy

Recommended events:

- `run.started`
- `agent.observed`
- `agent.decided`
- `message.sent`
- `message.received`
- `retrieval.started`
- `retrieval.completed`
- `tool.requested`
- `tool.completed`
- `policy.allowed`
- `policy.denied`
- `state.changed`
- `worker.failed`
- `retry.started`
- `verification.failed`
- `run.completed`

## 4. First-failure principle

Search for the earliest event that violates a contract or invariant.

Possible root-cause classes:

`RETRIEVAL | MODEL | TOOL | POLICY | STATE | COORDINATION | SECURITY | BUDGET | EXTERNAL_DEPENDENCY`

A downstream failure is often an innocent victim.

## 5. Deterministic replay

Capture enough metadata to reproduce the trajectory:

- exact input;
- model/configuration identifiers;
- tool responses or safe fixtures;
- retrieval result IDs and scores;
- policy version;
- state snapshot/version;
- random seeds where supported;
- timing/deadline information.

Replay should use recorded external results when investigating a historical incident. Otherwise the external world may have changed.

## 6. Differential debugging

Compare:

`expected trace` vs `actual trace`

Useful differences:

- different worker selected;
- missing retrieval result;
- changed tool arguments;
- policy decision changed;
- state transition diverged;
- retry count changed;
- latency budget exceeded.

## 7. Causal graph

Represent events as a directed graph:

```text
Task
 ├── Supervisor decision
 │     ├── Worker A
 │     │     ├── Retrieval
 │     │     └── Tool
 │     └── Worker B
 └── Aggregator
       └── Verifier
```

Use `causation_id` rather than relying solely on timestamps.

## 8. Detailed labs

### Lab 1 — Trace schema
Implement a versioned event schema and validation.

### Lab 2 — First failure detector
Given a trajectory containing multiple errors, identify the earliest invariant violation.

### Lab 3 — Wrong worker routing
Inject a supervisor routing error and trace its downstream impact.

### Lab 4 — Retrieval regression
Change index version and demonstrate degraded evidence quality.

### Lab 5 — Tool argument mutation
Inject an incorrect argument between decision and execution. Detect the mismatch.

### Lab 6 — State corruption
Modify a child state version and identify the invalid transition.

### Lab 7 — Duplicate execution
Use trace events to find duplicate side effects caused by message replay.

### Lab 8 — Latency investigation
Break down p95 latency into queue, model, retrieval, tool and verification components.

### Lab 9 — Cost investigation
Find which worker or retry loop caused a cost spike.

### Lab 10 — Security incident
Trace an indirect prompt injection from retrieved content through a proposed tool call and show where policy should have blocked it.

### Lab 11 — Deterministic replay
Replay a historical run from fixtures and verify the same control-flow decision.

### Lab 12 — Regression generation
Convert the incident into an automated test and add it to the benchmark suite.

## 9. Failure injection matrix

| Injected failure | Expected diagnosis |
|---|---|
| wrong worker | coordination/routing |
| stale retrieval | retrieval/index |
| malformed output | contract |
| bad tool args | model/orchestration |
| unauthorized action | policy/security |
| stale state | state consistency |
| duplicate task | idempotency |
| slow dependency | external/latency |
| recursive retry | orchestration/budget |
| poisoned document | security/retrieval |

## 10. Production debugging workflow

1. Freeze the incident window.
2. Identify affected run IDs and tenants.
3. Reconstruct the causal graph.
4. Find the first invariant violation.
5. Separate root cause from downstream symptoms.
6. Contain the affected capability/path.
7. Replay with safe fixtures.
8. Patch the control layer.
9. Add a regression case.
10. Verify the fix against neighboring workloads.

## 11. Observability metrics

- trace completeness;
- missing-event rate;
- first-failure classification accuracy;
- replay reproducibility;
- p50/p95/p99 latency by component;
- token/cost by agent;
- retry amplification;
- duplicate side-effect rate;
- policy-denial rate;
- verification failure rate;
- mean time to diagnose.

## 12. Security and privacy

Debugging data can become a second security problem. Apply:

- secret redaction;
- tenant isolation;
- data minimization;
- access-controlled traces;
- retention policies;
- immutable audit records for sensitive actions;
- safe fixtures for replay.

Never solve observability by copying every production secret into a log.

## 13. Industry scenarios

**Banking:** reconstruct why a transaction recommendation changed without exposing customer secrets.

**Healthcare:** determine whether a wrong summary originated in retrieval, extraction or generation while preserving patient isolation.

**Cybersecurity:** trace a suspicious autonomous remediation request from untrusted evidence to blocked policy decision.

**Enterprise IT:** identify whether an outage was caused by agent routing, tool latency or a bad state transition.

## 14. Interview questions

1. What is the first-failure principle?
2. Why is the final error often not the root cause?
3. What belongs in an agent trace?
4. How do you replay a nondeterministic system?
5. Why are causation IDs better than timestamps alone?
6. How do you debug retrieval vs generation failures?
7. How do you investigate duplicate side effects?
8. How do you debug a cost spike?
9. How do you protect trace data?
10. How would you design distributed tracing for 100 agents?
11. What makes a regression test useful after an incident?
12. How do you compare two agent versions?
13. How do you debug an indirect prompt injection?
14. What should be recorded for model/tool versioning?
15. How do you separate model uncertainty from infrastructure failure?

## 15. System-design challenge

Design an observability and debugging platform for a 100-agent enterprise system. It must support distributed traces, causal graphs, replay, tenant isolation, cost/latency analysis, security investigation and regression-test generation.

## 16. Coding challenges

- Trace-event validator
- Causal graph builder
- First-failure classifier
- Trace diff engine
- Replay fixture store
- Latency waterfall calculator
- Cost attribution engine
- Retry amplification detector
- Security incident correlator
- Regression-case generator

## 17. Mastery gate

You pass when you can take a complex failed run and produce:

- causal timeline;
- first invariant violation;
- root-cause classification;
- blast radius;
- containment action;
- reproducible replay;
- code/control fix;
- regression test;
- evidence that the fix worked.

## Gold challenge

Build **AegisAI Distributed Agent Debugger**: ingest structured trajectories, construct the causal graph, identify first failure, attribute latency/cost/security impact, replay the run with safe fixtures and automatically generate a regression test.
