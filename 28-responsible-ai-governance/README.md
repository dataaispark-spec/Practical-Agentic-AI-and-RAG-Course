# Module 28 — Responsible AI + Security: AI Governance Layer

## Mission

Turn AegisAI's technical controls into an enterprise governance system. The governance layer decides **who may use which AI capability, for what purpose, with what data, under which risk controls, and with what evidence and human oversight**.

This module is framework-neutral and implementation-first.

## Core mental model

```text
Business purpose
      ↓
Risk classification
      ↓
Data / privacy classification
      ↓
Model + tool eligibility
      ↓
Policy decision
      ↓
Human oversight / approval
      ↓
Execution
      ↓
Monitoring + audit
      ↓
Incident / remediation
      ↓
Periodic re-evaluation
```

Governance is not a PDF policy sitting beside the system. **Governance is executable control.**

## Learning outcomes

By the end, learners can:

- classify AI use cases by risk;
- translate policies into deterministic controls;
- separate policy from model judgment;
- implement human-in-the-loop thresholds;
- enforce data classification and purpose limitation;
- design model/vendor eligibility rules;
- maintain audit evidence;
- build incident and exception workflows;
- test governance controls adversarially;
- connect security, evaluation, observability and cost controls;
- design governance for autonomous agents and long-running workers.

## Governance dimensions

Every AegisAI task should be evaluated across:

| Dimension | Example question |
|---|---|
| Purpose | Is this use case approved? |
| User | Who is requesting it? |
| Data | What classification is entering the model? |
| Model | Is the selected model approved? |
| Tool | Which external capability can be invoked? |
| Action | Is the action informational or consequential? |
| Geography | Are residency/location constraints satisfied? |
| Risk | What harm could failure create? |
| Oversight | Is human approval mandatory? |
| Evidence | Can the decision be reconstructed? |
| Monitoring | What signals trigger intervention? |
| Lifecycle | When must the control be revalidated? |

## Risk tiers

Educational baseline:

- **R0 — Experimental:** sandbox only, synthetic/non-sensitive data.
- **R1 — Low impact:** informational assistance with limited consequences.
- **R2 — Controlled:** sensitive business data or consequential recommendations.
- **R3 — High impact:** decisions/actions with material financial, safety, legal, employment or customer consequences.
- **R4 — Prohibited/restricted:** use cases blocked by organizational policy or applicable requirements.

The exact classification must be defined by the organization's policy and jurisdiction; the course does not claim that this taxonomy itself is a legal standard.

## Policy precedence

Use a deterministic precedence order:

**law/mandatory controls → organizational policy → authorization → privacy/data controls → safety → task constraints → optimization.**

A model must never be allowed to negotiate these controls.

## Labs — 15 detailed builds

### Lab 1 — AI use-case registry
Create a registry containing owner, purpose, users, data classes, models, tools, risk tier and approval state.

### Lab 2 — Risk classifier
Build deterministic rules for informational, sensitive and high-impact workflows. Include explicit unknown/needs-review outcomes.

### Lab 3 — Policy engine
Translate governance requirements into allow/deny/approval decisions.

### Lab 4 — Data classification gate
Block a model route when input data is more sensitive than the model's approved trust tier.

### Lab 5 — Model/vendor eligibility
Create an allowlist based on capability, geography, privacy, contractual status and risk tier.

### Lab 6 — Human oversight
Require exact, contextual approval for high-impact actions. Test approval replay and action mutation.

### Lab 7 — Explainability evidence
Record why a route/action was permitted, blocked or escalated without pretending that an LLM's hidden reasoning is a reliable audit artifact.

### Lab 8 — Audit ledger
Build append-only governance events and reconstruct a complete decision timeline.

### Lab 9 — Exceptions
Create time-bound, scoped exceptions with owner, reason, expiry and compensating controls.

### Lab 10 — Incident management
Map security/evaluation failures to incidents, severity, containment, owner, remediation and regression tests.

### Lab 11 — Continuous monitoring
Build governance signals for policy violations, unsafe outputs, drift, unusual tool usage and approval anomalies.

### Lab 12 — Third-party model review
Create a model intake checklist: capability, data handling, residency, security, reliability, evaluation, cost and contractual controls.

### Lab 13 — Agent governance
Govern memory, tools, MCP servers, autonomous loops, delegation and computer-use permissions.

### Lab 14 — Red-team governance benchmark
Attack policy boundaries using prompt injection, tool poisoning, privilege escalation, data exfiltration and approval bypass attempts.

### Lab 15 — Governance release certification
Produce a release packet containing model/version, dataset, evaluation results, security findings, policy status, owner, residual risks and rollback plan.

## Failure-first exercises

Intentionally break the governance layer:

1. model output overrides a deny policy;
2. cheap model receives restricted data;
3. approval is reused for a modified action;
4. expired exception remains active;
5. audit event is missing;
6. tenant crosses a policy boundary;
7. tool result is incorrectly trusted;
8. high-impact workflow lacks human review;
9. governance blocks safe low-risk work unnecessarily;
10. monitoring samples away the only policy violation;
11. model version changes without re-evaluation;
12. policy configuration changes without an audit trail;
13. agent delegates to an unapproved capability;
14. memory contains prohibited data;
15. incident closes without a regression test.

## Governance control plane

Connect previous modules:

```text
Module 18 Security
       +
Module 25 Observability
       +
Module 26 Evaluation
       +
Module 27 Cost
       ↓
AI Governance Control Plane
       ↓
Model / RAG / Agent / MCP / Computer Use
```

## Production metrics

Track:

- policy decision volume;
- deny rate;
- approval rate;
- approval latency;
- policy violation rate;
- high-risk action rate;
- exception count and age;
- audit completeness;
- incident recurrence;
- evaluation regression rate;
- model inventory coverage;
- data classification coverage;
- human override rate;
- unsafe-action prevention rate.

## Security and privacy principles

- deny by default for unknown capabilities;
- least privilege;
- purpose limitation;
- data minimization;
- tenant isolation;
- explicit trust boundaries;
- no secrets in untrusted model context;
- exact approval binding;
- immutable/auditable evidence;
- controlled egress;
- lifecycle expiry;
- independent verification for consequential actions.

## Industry scenarios

**Banking:** governance around customer data, financial recommendations, payment actions and fraud workflows.

**Healthcare:** evidence requirements, privacy controls, human oversight and strict action boundaries.

**Cybersecurity:** autonomous investigation may be allowed while destructive remediation remains approval-gated.

**Enterprise IT:** agents can diagnose broadly but receive narrowly scoped production mutation permissions.

## Interview bank

1. What does AI governance mean operationally?
2. Why isn't an AI policy document enough?
3. How do you classify AI risk?
4. Which controls must be deterministic?
5. How do you govern third-party models?
6. How do you govern autonomous agents?
7. How do you prevent approval replay?
8. What belongs in an AI audit trail?
9. How do exceptions work safely?
10. How do security and governance differ?
11. How do you prove a policy was enforced?
12. How would you govern 10,000 AI use cases?
13. How do you handle a model update?
14. How do you balance governance and developer velocity?
15. What happens when governance itself fails?

## System-design challenge

Design an enterprise AI governance plane for 5,000 employees, 200 AI applications, 30 model providers and hundreds of tools. It must support centralized policy with local ownership, tenant isolation, auditability, emergency blocking, exceptions, evaluation gates and autonomous agents.

## Coding challenge

Implement:

- risk registry;
- policy evaluator;
- data-classification gate;
- model eligibility filter;
- approval store;
- exception manager;
- audit ledger;
- incident workflow;
- governance regression suite.

## Mastery gate

Given an AI application with sensitive data, external tools, autonomous actions and multiple model providers, produce an executable governance architecture that can **prove** which policies were applied and why every consequential action was allowed, denied or escalated.

## Gold challenge

Build **AegisAI Governance Control Plane** and integrate Modules 18, 25, 26 and 27. The final system should make governance decisions before execution, record evidence, enforce approvals, detect violations, trigger incidents and block releases when safety/evaluation requirements fail.
