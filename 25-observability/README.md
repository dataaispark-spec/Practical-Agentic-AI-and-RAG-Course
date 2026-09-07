# Module 25 — Observability: AI Observability Platform

## Mission

Build the telemetry control plane for AegisAI. Observe an AI system end-to-end rather than treating the LLM as a black box.

```text
User
 ↓
Agent Loop → RAG → Model → Tools → MCP → External Systems
 ↓          ↓       ↓       ↓       ↓
 traces    spans   metrics  events  audits
              ↓
      AI Observability Platform
              ↓
   dashboards / alerts / debugging
```

## Learning outcomes

- Design AI-specific traces, spans and metrics.
- Correlate agent, RAG, tool, MCP and distributed-agent events.
- Attribute latency and cost to individual components.
- Track quality signals alongside infrastructure signals.
- Detect retry storms, loops and anomalous tool use.
- Build actionable alerts rather than noisy dashboards.
- Preserve security, privacy and tenant boundaries.
- Feed telemetry into Module 22 debugging and Module 26 evaluation.

## Why ordinary observability is insufficient

Traditional telemetry answers **"is the service healthy?"**

Agentic observability must also answer:

- Did the agent accomplish the task?
- Which evidence influenced the answer?
- Which tool was selected and why?
- Was the action authorized?
- Did the verifier accept it?
- How much did the run cost?
- Where did latency accumulate?
- Did the agent loop unnecessarily?
- Did an untrusted input cross a security boundary?

## Canonical trace

```text
run
 ├─ agent.observe
 ├─ agent.decide
 ├─ retrieval
 │   ├─ query
 │   └─ ranking
 ├─ model
 ├─ tool
 │   └─ MCP server
 ├─ state
 ├─ verification
 └─ completion
```

Every span should carry correlation identifiers and safe metadata.

## Core telemetry model

### Traces
End-to-end causal execution.

### Spans
Component-level operations with start/end time and status.

### Metrics
Aggregated signals such as p95 latency, token usage and error rate.

### Events
Discrete security, policy, approval, retry and lifecycle events.

### Logs
Human-readable diagnostic context, with strict redaction.

## AI-specific metrics

### Reliability
- task success rate;
- completion/error rate;
- retry rate;
- timeout rate;
- duplicate action rate.

### Quality
- groundedness;
- citation correctness;
- retrieval Recall@K;
- verifier pass rate;
- human escalation rate.

### Performance
- p50/p95/p99 latency;
- queue time;
- model latency;
- retrieval latency;
- tool latency;
- critical-path duration.

### Economics
- input/output tokens;
- cost/run;
- cost/agent;
- cost/tool;
- cost/successful task;
- retry amplification.

### Security
- policy denials;
- approval failures;
- injection detections;
- cross-tenant attempts;
- suspicious tool sequences;
- secret-redaction events.

## Detailed labs

### Lab 1 — Telemetry contract
Define versioned trace/span/event schemas.

### Lab 2 — End-to-end trace
Instrument an agent run across model, retrieval and tool calls.

### Lab 3 — Critical path
Calculate sequential and parallel latency contribution.

### Lab 4 — Cost attribution
Attribute tokens and tool costs to agents and tasks.

### Lab 5 — Quality + infrastructure correlation
Show how a retrieval latency spike affects task success.

### Lab 6 — Loop detection
Detect repeated states/tool calls before the budget is exhausted.

### Lab 7 — Retry storm
Inject a failing dependency and measure retry amplification.

### Lab 8 — Security telemetry
Detect an indirect injection and trace the attempted capability escalation.

### Lab 9 — Tenant-safe observability
Prevent one tenant from querying another tenant's telemetry.

### Lab 10 — Alert engineering
Build alerts for SLO violations, security events and abnormal costs.

### Lab 11 — Dashboard design
Create an executive view and an engineer-debugging view.

### Lab 12 — Debugger integration
Send traces into Module 22 and locate the first causal failure.

### Lab 13 — Evaluation integration
Attach Module 26 quality/evaluation outcomes to execution traces.

### Lab 14 — Sampling
Compare full, head-based and tail-based trace sampling while preserving important failures.

### Lab 15 — Incident response
Use telemetry to write an incident timeline, root cause, blast radius and remediation plan.

## Failure-first exercises

Break observability deliberately:

- missing parent span;
- incorrect timestamps;
- duplicate events;
- dropped security event;
- cross-tenant trace query;
- unredacted secret;
- misleading success metric;
- missing tool cost;
- trace sampling hides the failure;
- clock skew;
- retry storm floods telemetry;
- model version missing from trace.

## Production architecture challenge

Design a multi-region telemetry platform with:

- ingestion gateway;
- event validation;
- durable queue;
- hot trace store;
- long-term metrics store;
- tenant isolation;
- retention policy;
- sampling;
- alert engine;
- dashboard/API layer;
- security/audit stream.

Separate the **control plane** from the **data plane** and define what happens when telemetry itself is unavailable.

## Security/privacy

Observability must not become a data-exfiltration channel.

Apply:

- field-level redaction;
- secret/token removal;
- PII minimization;
- tenant-scoped queries;
- role-based access;
- retention limits;
- immutable security events;
- safe replay fixtures.

## Interview bank

1. Why does an agent need different observability from a normal API?
2. Trace vs span vs event vs metric?
3. What belongs in an LLM span?
4. How do you attribute cost across parallel agents?
5. How do you detect loops?
6. What is tail-based sampling?
7. How do you preserve security events under sampling?
8. How would you observe 100,000 concurrent agents?
9. What if telemetry storage goes down?
10. How do you prevent telemetry from leaking PII?
11. How do quality and infrastructure metrics interact?
12. How do you design alerts that engineers will not ignore?

## Coding challenges

- trace validator;
- span duration calculator;
- critical-path engine;
- cost attribution engine;
- retry-amplification detector;
- loop detector;
- anomaly detector;
- tenant-safe query filter;
- redaction pipeline;
- SLO evaluator.

## Mastery gate

Given a failed AegisAI run, reconstruct the execution, identify the critical path, attribute cost, identify quality degradation, detect security signals and produce an actionable alert plus incident report.

## Gold challenge

Build **AegisAI Observability Platform** that receives structured telemetry from Modules 18–24, supports causal debugging, cost/latency/quality analysis and security investigation, and provides the evaluation-ready dataset required by Module 26.
