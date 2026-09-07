# Module 29 — Deployment + CI/CD: Production Deployment Pipeline

## Mission

Take the AegisAI components built in Modules 1–28 from repository code to a controlled production release.

The goal is not merely `docker build`. The goal is **repeatable, observable, reversible and policy-gated delivery of AI systems**.

## Production pipeline

```text
Developer change
      ↓
Lint / type / unit tests
      ↓
Security + dependency checks
      ↓
Build immutable artifact
      ↓
Integration tests
      ↓
RAG / agent evaluation
      ↓
Governance + policy gate
      ↓
Shadow / canary
      ↓
Production
      ↓
Telemetry + SLOs
      ↓
Rollback / remediation
```

## Learning outcomes

- Containerize AI services reproducibly.
- Separate configuration from code.
- Handle secrets correctly.
- Build health/readiness checks.
- Design CI quality gates.
- Add evaluation/security/governance gates to deployment.
- Perform migrations safely.
- Use immutable versioned artifacts.
- Design canary, shadow and rollback strategies.
- Handle model, prompt, retrieval and policy version changes.
- Operate production incidents and recovery.

## AI-specific deployment reality

A normal software release may change a binary. An AI release can change:

- model version;
- prompt/versioned instructions;
- retrieval corpus;
- embedding model;
- reranker;
- tool schema;
- MCP server;
- policy;
- memory schema;
- evaluator/judge;
- routing/cost configuration.

Therefore an AegisAI release identity must capture **the complete execution contract**, not only an application version.

## Release manifest

A production release should identify:

```text
application version
container digest
model/provider/version
prompt version
retrieval/index version
embedding/reranker versions
tool/MCP versions
policy version
evaluation dataset/version
governance status
configuration version
migration version
```

## Deployment environments

### Local
Fast developer feedback with synthetic data.

### CI
Deterministic automated checks.

### Staging
Production-like integrations and realistic failure injection.

### Shadow
Observe candidate behavior without affecting user-visible decisions.

### Canary
Small controlled production traffic allocation.

### Production
Full traffic subject to operational gates.

## Labs — 15 detailed builds

### Lab 1 — Reproducible service
Containerize an AegisAI service with a non-root runtime and deterministic dependency installation.

### Lab 2 — Configuration separation
Move environment-specific configuration out of source code and validate required settings at startup.

### Lab 3 — Secrets discipline
Use secret references rather than embedding credentials in images, notebooks or Git history.

### Lab 4 — Health endpoints
Implement liveness, readiness and dependency health semantics.

### Lab 5 — CI unit gate
Run deterministic unit and contract tests on every change.

### Lab 6 — Integration gate
Exercise model, RAG, tool and policy boundaries using test doubles.

### Lab 7 — Security gate
Fail the pipeline for critical security regressions.

### Lab 8 — Evaluation gate
Connect Module 26 regression evaluation and block releases below quality/safety thresholds.

### Lab 9 — Governance gate
Connect Module 28 and block unauthorized model, data or capability configurations.

### Lab 10 — Artifact promotion
Build once, identify by immutable digest, then promote the same artifact across environments.

### Lab 11 — Database/state migration
Design backward-compatible migrations and restart-safe state transitions.

### Lab 12 — Shadow deployment
Compare candidate and incumbent traces, cost, latency, safety and quality.

### Lab 13 — Canary rollout
Route a small percentage of traffic and define automatic abort thresholds.

### Lab 14 — Rollback drill
Intentionally introduce a bad model/prompt/policy release and restore the previous known-good version.

### Lab 15 — Production incident
Simulate elevated latency, model failure, policy regression, tool outage and cost explosion; execute the runbook.

## Failure-first exercises

Break the deployment system intentionally:

1. latest dependency introduces a regression;
2. secret accidentally appears in logs;
3. readiness passes while a critical dependency is unavailable;
4. model version changes without evaluation;
5. prompt changes without release identity;
6. vector index is incompatible with embedding version;
7. migration cannot roll forward/back;
8. canary receives an unrepresentative workload;
9. rollback restores application code but not model configuration;
10. CI skips a security test;
11. governance policy is stale;
12. health check causes restart storm;
13. deployment doubles cost;
14. partial rollout leaves incompatible workers;
15. telemetry is unavailable during an incident.

## CI quality gates

Minimum recommended order:

**format → type → unit → integration → security → evaluation → governance → build → deploy.**

Not every organization needs every stage, but the important principle is that **deployment must be downstream of evidence**.

## SLOs

Track:

- availability;
- p50/p95/p99 latency;
- error rate;
- task success;
- groundedness;
- citation correctness;
- security violation rate;
- cost per successful task;
- rollback time;
- deployment frequency;
- change failure rate;
- recovery time.

## AI rollback dimensions

Rollback can mean reverting:

- application;
- model;
- prompt;
- retrieval index;
- embedding/reranker;
- tool/MCP version;
- policy;
- routing configuration.

A sophisticated platform can roll back one dimension without blindly reverting all others.

## Industry scenarios

**Banking:** release gates for sensitive customer workflows and controlled production changes.

**Healthcare:** evaluation, privacy and governance gates before model promotion.

**Cybersecurity:** rapid rollback when an agent/tool release increases unsafe actions.

**Enterprise IT:** canary deployment for high-volume support agents and production remediation workflows.

## Interview bank

1. What makes AI CI/CD different from conventional CI/CD?
2. What belongs in an AI release manifest?
3. Why build once and promote by immutable digest?
4. How do you deploy a new model safely?
5. How do you roll back a prompt?
6. How do you handle embedding/index incompatibility?
7. What is shadow versus canary deployment?
8. How should evaluation block deployment?
9. What belongs in readiness versus liveness?
10. How do you prevent secret leakage?
11. How do you perform zero-downtime migration?
12. How would you deploy an agent used by millions of users?
13. How do you detect a bad release quickly?
14. How do you rollback policy without creating a security hole?
15. What metrics define deployment health?

## System-design challenge

Design a production delivery platform for AegisAI serving multiple tenants with separate policies and data. It must support model/prompt/RAG/tool releases, automated evaluation, security/governance gates, canary, rollback, audit and incident response.

## Coding challenges

- release manifest validator;
- configuration validator;
- health/readiness checker;
- CI gate aggregator;
- deployment state machine;
- canary evaluator;
- rollback planner;
- migration compatibility checker;
- secret scanner test;
- release certification report.

## Mastery gate

Given a failing production release caused by a model, prompt, retrieval, policy or infrastructure change, identify the first failure, contain it, choose the correct rollback dimension, restore service and produce evidence that the repaired release is safe.

## Gold challenge

Build the **AegisAI Production Delivery Pipeline** integrating Modules 18, 25, 26, 27 and 28. A release should be impossible when critical security, evaluation or governance gates fail, while emergency rollback remains fast and auditable.
