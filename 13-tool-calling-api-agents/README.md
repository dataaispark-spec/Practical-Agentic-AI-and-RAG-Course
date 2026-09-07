# Module 13 — Tool Calling + API Agents

## Mission
Turn an LLM from a text generator into a controlled system that can request real operations through typed, validated and authorized tools.

## Mental model
```text
User goal
  ↓
Model decides whether a tool is needed
  ↓
Tool call schema
  ↓
Validation
  ↓
Policy / authorization
  ↓
Idempotency + budget checks
  ↓
Tool execution
  ↓
Structured tool result
  ↓
Model continues
```

The model **requests** an action. Application code decides whether that action is permitted and how it executes.

## Learning outcomes
Build a framework-free tool runtime supporting:
- typed tool schemas;
- tool registration/discovery;
- argument validation;
- deterministic authorization;
- risk classification;
- idempotency;
- timeout/retry behavior;
- structured errors;
- audit events;
- tool-result contracts;
- human approval for high-impact actions.

## Tool contract
Every tool should define:
- name;
- description;
- input schema;
- output schema;
- risk class;
- required permissions;
- timeout;
- retry policy;
- idempotency policy;
- audit requirements.

## Tool categories
### Read-only
Search, retrieve, calculate, inspect status.

### Reversible write
Create draft, update a non-critical record, schedule a reversible operation.

### Irreversible/high-impact
Transfer funds, delete data, send external communication, change production configuration. These require deterministic policy and usually approval.

## Labs
### Lab 1 — Tool registry
Register `search_customer`, `get_order`, `calculate_refund` and `create_refund` with typed contracts.

### Lab 2 — Schema validation
Reject missing, extra, wrong-type and out-of-range arguments.

### Lab 3 — Tool selection
Given 20 natural-language requests, classify which tool is appropriate and create a gold decision set.

### Lab 4 — Authorization
Create roles such as support-agent, manager and finance-admin. Prove unauthorized calls fail before execution.

### Lab 5 — Risk gates
Require human approval for refunds above a threshold and all irreversible operations.

### Lab 6 — Idempotency
Send the same tool request twice. Prove that the side effect happens once.

### Lab 7 — Timeout/retry
Inject transient and permanent failures. Retry only retryable failures and preserve the original request ID.

### Lab 8 — Structured errors
Return machine-readable errors such as `VALIDATION_ERROR`, `NOT_FOUND`, `POLICY_DENIED`, `RATE_LIMITED` and `UPSTREAM_TIMEOUT`.

### Lab 9 — Tool injection
Put malicious instructions inside a tool result. Demonstrate that tool output is untrusted data and cannot override system policy.

### Lab 10 — Complete Data Agent
Build an agent that searches customer/order data, reasons over the results, and requests a refund only when policy permits.

## Detailed exercises
1. Design a JSON schema for a financial transfer.
2. Add enum validation for risk levels.
3. Build a registry lookup by tool name.
4. Implement permission checks.
5. Implement idempotency keys.
6. Add timeout handling.
7. Add exponential retry with bounded attempts.
8. Add structured audit records.
9. Add approval state persistence.
10. Prevent a model from directly executing arbitrary Python.
11. Create a malicious tool result and test policy isolation.
12. Build a tool simulator for 100 generated calls.
13. Measure tool success/error/latency rates.
14. Build a deterministic fallback when a tool is unavailable.
15. Design tool version compatibility.

## Failure-first exercises
- malformed JSON arguments;
- unknown tool name;
- unauthorized tool;
- stale resource ID;
- duplicate delivery;
- partial upstream failure;
- timeout after side effect;
- malicious tool output;
- excessive tool-call loop;
- tool result larger than context budget.

## Tool-call loop
```text
OBSERVE state
 ↓
DECIDE tool or answer
 ↓
VALIDATE request
 ↓
POLICY CHECK
 ↓
APPROVAL if needed
 ↓
EXECUTE
 ↓
VERIFY result
 ↓
continue / stop
```

## Production requirements
- never expose unrestricted credentials to the model;
- keep secrets outside prompts/tool arguments;
- validate server-side even when the model generated a schema-valid call;
- enforce budgets outside the model;
- make writes idempotent where possible;
- record authorization decisions;
- separate tool identity from user identity;
- use least privilege;
- isolate tenants;
- verify side effects.

## Industry labs
**Banking:** account lookup + transaction simulation + approval-gated transfer.

**Healthcare:** patient-record search with role-based access and audit logging.

**Cybersecurity:** incident lookup + safe diagnostic actions + production-change approval.

**Manufacturing:** equipment telemetry + maintenance-ticket creation.

**Enterprise IT:** ticket search + knowledge retrieval + controlled remediation.

## Interview questions
1. What is tool calling?
2. Why are schemas necessary?
3. Who should enforce authorization?
4. Why can't model-generated JSON be trusted?
5. Explain idempotency.
6. How do you handle timeout-after-side-effect?
7. What should a tool result contain?
8. How do you secure credentials?
9. How do you prevent arbitrary tool execution?
10. How do you classify tool risk?
11. How do you design approval workflows?
12. How do you version tools?
13. How do you debug tool-selection failures?
14. How do you cap tool loops?
15. How would you test 1,000 tool calls?

## System-design challenge
Design a tool gateway serving 500 agents and 2,000 tools with strict tenant isolation, role-based authorization, approval workflows, rate limits, idempotency, auditability and p95 tool dispatch under 100 ms before upstream execution.

## Mastery gate
You pass when you can build a safe tool runtime without relying on the model to enforce policy, demonstrate duplicate/timeout recovery, and explain exactly where authorization, verification and audit happen.

## Google Colab
`notebooks/module_13_tool_calling.ipynb` is self-contained and implements typed tools, validation, authorization, risk gates, idempotency, failure injection and a mini Data Agent.
