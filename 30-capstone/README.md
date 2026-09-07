# Module 30 — Capstone: AegisAI Complete Enterprise Agentic RAG Platform

## Mission

Integrate the engineering disciplines from Modules 1–29 into one production-oriented enterprise AI platform.

This is **not a larger chatbot**. It is a controlled AI system with retrieval, tools, agents, state, security, evaluation, observability, economics, governance and deployment controls.

## AegisAI mental model

```text
                    ┌──────────────────────┐
                    │      User / API       │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Goal + Task Contract  │
                    └──────────┬───────────┘
                               ↓
       ┌───────────────────────┼────────────────────────┐
       ↓                       ↓                        ↓
   Governance              Security                 Budget
       │                       │                        │
       └───────────────────────┼────────────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │    Agent Harness     │
                    │ observe/decide/act   │
                    │ verify/recover       │
                    └──────────┬───────────┘
                               ↓
       ┌───────────────┬───────┼────────┬───────────────┐
       ↓               ↓       ↓        ↓               ↓
      RAG            Memory   Tools     MCP           Models
       │               │       │        │               │
       └───────────────┴───────┼────────┴───────────────┘
                               ↓
                         Verification
                               ↓
                Observability + Evaluation
                               ↓
                     Durable Execution
                               ↓
                       Production Deploy
```

## Capstone objectives

Build a multi-tenant enterprise assistant that can:

- answer grounded questions from enterprise documents;
- retrieve evidence with ACL enforcement;
- call approved tools;
- plan and execute multi-step work;
- preserve durable state;
- request human approval for consequential actions;
- recover from crashes and transient failures;
- enforce security and data boundaries;
- control cost and resource budgets;
- evaluate every release;
- expose production telemetry;
- support shadow/canary rollout and rollback;
- reconstruct an auditable action history.

## Reference enterprise scenario

Use one synthetic but realistic organization. Recommended domains:

- Banking operations;
- Healthcare operations;
- Cybersecurity SOC;
- Enterprise IT service management.

The same platform must support at least **two domains** without hard-coding domain-specific agent behavior into the core runtime.

## Required architecture

### 1. API boundary

Typed request/response contracts, authentication context, tenant binding, request IDs and deadlines.

### 2. Task contract

Every task has goal, constraints, risk, budget, tenant, allowed capabilities and completion criteria.

### 3. Governance gate

Policy must run before model/tool execution. High-risk actions require exact approval.

### 4. Agent harness

Explicit loop:

`OBSERVE → DECIDE → ACT → VERIFY → RECOVER / CONTINUE / STOP`

No uncontrolled while-loop and no implicit infinite retries.

### 5. RAG subsystem

Document ingestion → normalization → chunking → embeddings → hybrid retrieval → reranking → evidence → grounded generation.

### 6. Tool/MCP gateway

Capability discovery, authorization, validation, timeouts, retries, idempotency, trust labels and audit.

### 7. Memory

Working, episodic, semantic and procedural memory with provenance, confidence, TTL and tenant isolation.

### 8. Durable state

Checkpoint the run so a process restart does not silently restart the task from zero.

### 9. Verification

Verify evidence, tool effects, action contracts and task completion independently from the model's assertion of success.

### 10. Cost control

Enforce token/tool/time/money budgets and choose cost-efficient routes without weakening policy or security.

### 11. Observability

Trace model, retrieval, tool, MCP, state, policy and verification events into a causally reconstructable run.

### 12. Evaluation

Golden cases, trajectory evaluation, security evaluation, regression gates, A/B/shadow comparison and release certification.

### 13. Deployment

Immutable artifact, release manifest, CI gates, canary, rollback and incident runbook.

## Capstone phases — 15 labs

### Lab 1 — Requirements and threat model
Define users, domains, assets, trust boundaries, failure modes, abuse cases and success metrics.

**Deliverable:** architecture brief + threat model.

### Lab 2 — Contracts and API
Implement typed task/action/evidence/verification contracts.

**Deliverable:** API contract tests.

### Lab 3 — Enterprise RAG
Build ingestion, ACL-aware retrieval and citation-grounded answers.

**Deliverable:** retrieval benchmark + golden dataset.

### Lab 4 — Tool gateway
Implement capability registry, validation, authorization, idempotency and audit.

**Deliverable:** tool integration tests.

### Lab 5 — Agent harness
Implement explicit loop with budgets, termination, recovery and trajectory recording.

**Deliverable:** trajectory fixtures + failure tests.

### Lab 6 — Planning and HITL
Add planner/executor/verifier behavior and exact approval for high-impact actions.

**Deliverable:** approval replay/mutation tests.

### Lab 7 — Memory
Add durable multi-tier memory with provenance, TTL, contradiction handling and tenant isolation.

**Deliverable:** memory poisoning tests.

### Lab 8 — Multi-agent decision
Start with a single-agent baseline. Add specialist workers only where measured task success justifies coordination cost.

**Deliverable:** fair single-vs-multi-agent benchmark.

### Lab 9 — Security red team
Attack prompt injection, retrieval poisoning, tool poisoning, privilege escalation, data exfiltration, SSRF-style egress and approval bypass.

**Deliverable:** security regression suite.

### Lab 10 — Observability
Produce an end-to-end trace and diagnose deliberately injected failures.

**Deliverable:** incident investigation report.

### Lab 11 — Evaluation
Create golden cases and release gates for quality, groundedness, safety, latency and cost/success.

**Deliverable:** evaluation report + blocked-release demonstration.

### Lab 12 — Cost engineering
Implement cost attribution, tenant budgets, route optimization and anomaly detection.

**Deliverable:** monthly unit-economics report.

### Lab 13 — Governance
Implement use-case registry, risk tier, policy gate, model/tool eligibility and exception workflow.

**Deliverable:** governance certification packet.

### Lab 14 — Production deployment
Build CI gates, immutable release identity, shadow/canary rollout and rollback.

**Deliverable:** release runbook.

### Lab 15 — Chaos and recovery
Inject worker crash, provider outage, stale state, duplicate delivery, tool failure, retrieval degradation, policy regression and cost explosion.

**Deliverable:** resilience report proving recovery.

## Gold scenario

A banking operations user asks:

> “Investigate this customer case, retrieve the relevant internal policies, summarize the evidence, check account-related information through approved systems, recommend the next action, and if a consequential action is required ask me for approval.”

The platform must:

1. authenticate and bind the tenant;
2. classify risk/data;
3. retrieve only authorized evidence;
4. preserve provenance;
5. plan the work;
6. call only approved capabilities;
7. keep sensitive outputs within policy;
8. request exact approval when required;
9. execute idempotently;
10. verify the effect;
11. record the complete trace;
12. stay within budget;
13. survive restart;
14. produce an auditable final report.

## Required failure matrix

| Failure | Expected control |
|---|---|
| Prompt injection | Trust boundary + policy |
| Poisoned document | Provenance + retrieval controls |
| Unauthorized tool | Capability authorization |
| Tool timeout | Retry policy + deadline |
| Duplicate side effect | Idempotency |
| Worker crash | Checkpoint/recovery |
| Stale state | Version/lease validation |
| Budget exhaustion | Hard budget |
| Model outage | Fallback route |
| Bad retrieval | Evaluation + verifier |
| Unsafe action | Policy + HITL |
| Policy regression | Governance gate |
| Quality regression | Evaluation gate |
| Cost explosion | Budget + anomaly detection |
| Deployment regression | Canary + rollback |

## Required production scorecard

### Quality
- task success;
- retrieval Recall@K;
- groundedness;
- citation correctness;
- verifier pass rate.

### Reliability
- p50/p95/p99 latency;
- error rate;
- recovery success;
- retry amplification;
- availability.

### Economics
- cost/request;
- cost/success;
- budget utilization;
- cache hit rate;
- savings versus baseline.

### Security
- policy violations;
- unauthorized actions prevented;
- injection detection;
- cross-tenant attempts;
- secret leakage.

### Governance
- audit completeness;
- approval compliance;
- exception age;
- model inventory coverage;
- evaluation certification.

## 20 interview questions

1. Why is an agent more than an LLM?
2. Why is verification separate from generation?
3. Where should policy enforcement live?
4. How do you make agent loops terminate?
5. How do you recover a long-running task after a crash?
6. How do you prevent duplicate side effects?
7. How do you secure retrieved documents?
8. How do you evaluate agent trajectories?
9. When should multi-agent architecture be rejected?
10. How do MCP and authorization interact?
11. How do you control autonomous agent cost?
12. What belongs in a durable checkpoint?
13. How do you handle model/provider failure?
14. How do you prove an action was authorized?
15. How do you rollback a model or prompt independently?
16. How do you prevent memory poisoning?
17. How do you design tenant isolation?
18. What is the difference between shadow and canary?
19. How do you turn incidents into regression tests?
20. What evidence would you show an enterprise security reviewer?

## Final system-design challenge

Design AegisAI for:

- 10,000 enterprise users;
- 100+ tenants;
- 10 million documents;
- multiple model providers;
- 500+ tools/MCP capabilities;
- asynchronous long-running tasks;
- human approvals;
- strict audit requirements;
- 99.9% availability target;
- predictable monthly AI spend.

Defend every major tradeoff: consistency, latency, cost, quality, security, availability, operational complexity and developer velocity.

## Final coding challenge

Starting from the repository primitives, implement the complete vertical slice:

`API → governance → retrieval → planning → tool → verification → checkpoint → telemetry → evaluation → release gate`

Do not hide the control flow inside a framework. Frameworks may be adapters around the mechanisms.

## Final mastery gate

A learner passes only after demonstrating:

- a successful end-to-end task;
- grounded evidence;
- policy enforcement;
- exact approval;
- durable restart;
- idempotent side effects;
- security attack resistance;
- measurable evaluation;
- cost budget enforcement;
- trace reconstruction;
- controlled deployment;
- rollback;
- incident-to-regression conversion.

## Portfolio outcome

The final repository should be defensible in an engineering interview because every major architectural claim has:

**code + tests + experiment + metrics + failure analysis + tradeoff explanation.**

That is the standard for the complete Agentic AI + RAG engineering track.
