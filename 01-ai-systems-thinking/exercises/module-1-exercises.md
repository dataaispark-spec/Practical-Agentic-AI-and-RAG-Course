# Module 1 — Industry Hands-On Exercises

## Exercise 1 — Architecture triage

For each scenario choose the minimum sufficient architecture:

1. Rewrite incoming support emails into a standard format.
2. Answer employee questions from frequently changing internal policies.
3. Read order status from an API and explain it to a customer.
4. Investigate a security alert using several read-only data sources and recommend a response.
5. Conduct a complex research task requiring several independent specialist roles.

For each scenario submit:

```text
Chosen pattern:
Why it is sufficient:
Rejected simpler pattern:
Rejected more complex pattern:
Top risk:
Primary KPI:
```

### Expected learning signal

The student should be able to explain *why a simpler system is insufficient* before proposing a more complex one.

## Exercise 2 — Support assistant architecture

Design a multi-tenant enterprise support assistant that:

- answers from internal knowledge
- reads order status
- cannot modify orders
- must preserve tenant isolation
- must expose traceable evidence

Deliverables:

- architecture diagram
- request sequence
- trust boundaries
- failure-mode table
- KPI table

## Exercise 3 — Latency/cost trade-off

Design two architectures for the same workflow:

### Option A

- one larger model call
- more context
- higher per-request cost
- lower orchestration overhead

### Option B

- smaller model for routing
- retrieval before generation
- fallback to a larger model for difficult cases

Define:

- expected task-success hypothesis
- latency hypothesis
- cost hypothesis
- experiment to validate them

## Exercise 4 — Security boundary review

Given this architecture:

```text
User -> Agent -> Vector DB
             -> Refund API
             -> SQL DB
```

Find at least eight security/control weaknesses. Then redraw the architecture showing:

- authentication
- tenant authorization
- tool allowlists
- parameter validation
- deterministic policy checks
- approval boundary
- audit logging

## Exercise 5 — Failure investigation

A policy assistant has the following production symptoms:

- answer quality fell from normal levels
- model latency is unchanged
- retrieved chunk count is unchanged
- users report older policy answers

Build a diagnostic hypothesis tree and identify the first three experiments you would run.

## Exercise 6 — Defend an architecture

Record a five-minute explanation answering:

> Why did you choose RAG instead of fine-tuning or long-context prompting for your use case?

The explanation must use requirements, assumptions, measurements, and trade-offs—not framework names.

## Exercise 7 — Stretch challenge

Design an architecture for a high-risk financial operations assistant that can:

- investigate transactions
- retrieve policy
- calculate a recommendation
- prepare an action
- require human approval before execution

Explicitly separate:

```text
read -> reason -> recommend -> approve -> execute
```

## Solution quality rubric

| Dimension | Developing | Strong | Interview-ready |
|---|---|---|---|
| Requirements | vague | explicit | quantified where possible |
| Architecture | tool-centric | requirement-driven | trade-offs defended |
| Security | afterthought | controls listed | trust boundaries explicit |
| Evaluation | generic accuracy | task metrics | baseline + regression plan |
| Reliability | happy path | failures considered | degradation strategy |
| Observability | logs only | metrics + logs | end-to-end traceability |
| Communication | feature list | structured | concise evidence-based defense |
