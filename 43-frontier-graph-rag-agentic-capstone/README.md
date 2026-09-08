# Module 43 — Frontier Graph-RAG Agentic Capstone

## Purpose

Module 43 is the integration point for the course. It is not another isolated framework tutorial. It asks the learner to assemble the mechanisms developed across the course into a single governed system that can retrieve structured and unstructured knowledge, reason over relationships, plan work, use tools, maintain durable state, operate across long-running tasks, interact with computer environments when appropriate, verify outcomes, and improve under controlled evaluation.

The central engineering question is not **“How autonomous can the model be?”** It is **“How much useful autonomy can the system safely sustain while remaining observable, recoverable, verifiable, and economically defensible?”**

The capstone uses the course mental model:

> **Agent = Model + Harness + Environment + Tools + State + Policy + Budget + Verification**

The model supplies probabilistic reasoning. The harness supplies control. The environment supplies the real execution surface. Tools expose bounded capabilities. State supplies continuity. Policy constrains what is allowed. Budgets constrain resource consumption. Verification establishes whether the result is acceptable. The capstone succeeds when these pieces form explicit contracts rather than an opaque chain of prompts.

## What makes Module 43 different

Earlier modules study mechanisms separately. Module 43 studies their interactions and the failure modes created by those interactions.

A Graph-RAG system can retrieve the right documents but traverse the wrong relationship. A graph can contain correct facts but stale temporal validity. A hybrid retriever can improve recall while increasing contradictory evidence. A capable agent can form a plausible plan but operate on stale state. Durable execution can preserve state while accidentally replaying a side effect. Computer use can ground the model in a real interface while exposing new risks from dynamic UI state. A self-improvement loop can optimize a benchmark while degrading real-world behavior.

The capstone therefore treats **composition risk** as a first-class engineering problem.

The learner should be able to answer, for every major operation:

- What evidence was available?
- How was that evidence retrieved?
- Why did the system select this path?
- Which state was authoritative at the time of the decision?
- Which tool or environment action was permitted?
- Which policies were evaluated?
- Which side effects occurred?
- Which verifier accepted or rejected the result?
- What happens after interruption, timeout, contradiction, or restart?
- Which artifacts and versions produced the behavior?
- What evidence would justify changing the system?

## Learning outcomes

By the end of the capstone, the learner should be able to design and defend a frontier Graph-RAG agentic system that integrates:

1. **Knowledge graph reasoning** for entities, relationships, provenance, constraints, and multi-hop context.
2. **Hybrid retrieval** combining graph traversal, lexical retrieval, vector retrieval, filtering, and reranking according to the query type.
3. **A production harness** that manages context, tool access, state transitions, budgets, checkpoints, recovery, replay, and telemetry.
4. **Durable autonomy** so long-running work can pause, resume, recover from worker failure, and avoid duplicate side effects.
5. **Computer use** where an external application or interface is genuinely the best execution surface.
6. **Verification** at retrieval, planning, tool, state, and final-outcome boundaries.
7. **Controlled self-improvement** in which candidate changes are evaluated before promotion and can be rolled back.

These outcomes directly reflect the repository’s Module 43 objective vocabulary: frontier Graph-RAG capstone, knowledge graph, hybrid retrieval, harness, durable autonomy, computer use, verification, and self-improvement. fileciteturn679file0L2-L2

## Capstone system: AegisAI Frontier Graph-RAG

The reference system is **AegisAI Frontier Graph-RAG**, an enterprise assistant for complex investigations and operational workflows. The exact business domain may vary, but the system must contain a meaningful mixture of:

- unstructured documents;
- structured records;
- a typed knowledge graph;
- temporal and provenance information;
- lexical and vector indexes;
- agent state and checkpoints;
- bounded tools;
- an execution environment;
- policy enforcement;
- independent verification;
- observability;
- evaluation datasets;
- candidate-change promotion and rollback.

A useful reference workload is an investigation request such as:

> “Determine the current status of a supplier issue, identify the affected products and contracts, explain the evidence and timeline, compare current facts with policy, and prepare the next permitted operational action.”

That request is deliberately difficult. It requires entity resolution, multi-hop relationships, temporal reasoning, evidence gathering, contradictory-source handling, policy evaluation, planning, state management, and possibly a tool or computer action. It is therefore a better capstone than a simple question-answering demo.

## Reference architecture

```text
                           ┌─────────────────────────┐
                           │        User / Event      │
                           └────────────┬────────────┘
                                        │
                              request + identity
                                        │
                           ┌────────────▼────────────┐
                           │   Policy / Risk Gate    │
                           └────────────┬────────────┘
                                        │
                           ┌────────────▼────────────┐
                           │   Agent Harness         │
                           │ context / budget /     │
                           │ state / checkpoint      │
                           └───────┬───────┬─────────┘
                                   │       │
                   ┌───────────────┘       └──────────────────┐
                   │                                          │
          ┌────────▼────────┐                       ┌─────────▼────────┐
          │ Retrieval Plane │                       │ Execution Plane  │
          │ graph + lexical │                       │ tools + computer │
          │ + vector + rank │                       │ environment      │
          └───────┬─────────┘                       └─────────┬────────┘
                  │                                           │
          ┌───────▼──────────┐                    ┌──────────▼─────────┐
          │ Evidence Context │                    │ Durable State       │
          │ provenance       │                    │ checkpoint / lease │
          │ timestamps       │                    │ idempotency         │
          └───────┬──────────┘                    └──────────┬─────────┘
                  │                                           │
                  └────────────────┬──────────────────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │ Verification      │
                         │ factual / policy  │
                         │ action / outcome  │
                         └─────────┬─────────┘
                                   │
                         ┌─────────▼─────────┐
                         │ Audit + Evaluation│
                         │ trace / metrics   │
                         │ regression / cost │
                         └───────────────────┘
```

The architecture intentionally keeps **retrieval, execution, state, policy, and verification separate**. A model may propose a retrieval query, traversal, plan, or tool invocation, but those proposals do not become trusted facts merely because they are fluent.

## 1. Knowledge graph as a reasoning substrate

A graph is valuable when relationships carry decision-making meaning that is awkward to reconstruct from isolated text chunks.

For the capstone, define explicit node types such as:

- `Person`
- `Organization`
- `Product`
- `Contract`
- `Incident`
- `Requirement`
- `Policy`
- `Document`
- `System`
- `Location`
- `Event`

Then define typed relationships such as:

- `OWNS`
- `SUPPLIES`
- `AFFECTS`
- `GOVERNS`
- `MENTIONS`
- `DEPENDS_ON`
- `VIOLATES`
- `SUPERSEDES`
- `LOCATED_AT`
- `APPROVED_BY`
- `DERIVED_FROM`

The graph should also carry metadata such as provenance, source identifier, confidence or extraction status where relevant, creation time, effective time, expiration time, and version.

### Why typing matters

A flat graph can return superficially related nodes. A typed graph allows deterministic constraints such as:

> “Find active contracts supplied by the affected organization whose products are linked to the incident and whose governing policy is currently effective.”

That query contains semantics that should not depend entirely on a language model remembering which relationship means what.

### Provenance is part of the fact

For a production-quality knowledge graph, the statement:

`Supplier A -> SUPPLIES -> Product B`

is incomplete. The system should also know where the relationship came from and whether the supporting evidence is current.

A stronger representation is conceptually:

```text
subject: Supplier A
predicate: SUPPLIES
object: Product B
source: contract_2026_014
observed_at: 2026-08-20
valid_from: 2026-01-01
valid_to: 2026-12-31
status: active
```

The exact storage representation is implementation-dependent; the contract is not.

### Entity resolution

Graph quality collapses when the same real-world entity receives multiple identities. The capstone should explicitly test cases such as:

- “ABC Ltd.” versus “ABC Limited”;
- parent company versus subsidiary;
- product code changes;
- renamed business units;
- duplicated incident records.

Entity resolution should produce a decision with evidence and confidence rather than silently merging records. High-impact merges should be reviewable and reversible.

### Temporal knowledge

Current truth and historical truth are not interchangeable. The graph should distinguish at least:

- event time;
- observation time;
- effective time;
- expiration or supersession time.

Consider a policy that was effective from January through June and replaced in July. A query run in September should not cite the old rule as current merely because it has a stronger embedding similarity.

## 2. Graph-RAG: retrieval beyond nearest neighbors

Graph-RAG should not be reduced to “vector search plus a graph database.” The design should begin from query intent.

### Retrieval modes

A practical capstone can route queries into several retrieval modes:

**Lexical retrieval** is valuable for exact terminology, identifiers, names, error codes, clauses, and phrases.

**Vector retrieval** is valuable for semantic similarity when terminology varies.

**Graph retrieval** is valuable when relationships, constraints, provenance, and multi-hop paths determine relevance.

**Hybrid retrieval** combines these signals when no single retrieval mode is sufficient.

The right question is not “Which retriever is best?” but:

> “Which evidence-generation strategy best matches this query and this failure cost?”

### Candidate generation versus ranking

Keep these concepts separate.

Candidate generation should maximize the chance that relevant evidence enters the pool. Ranking should decide which evidence is most useful for the final context.

For example:

```text
query
  ├── BM25 / lexical → candidates A, B, C, D
  ├── vector search → candidates B, D, E, F
  └── graph traversal → paths through B, E, G
                    ↓
                union / dedupe
                    ↓
              reranking
                    ↓
            context selection
```

A system that reranks only what vector retrieval returned cannot recover a critical exact-match document that never entered the candidate pool.

### Reciprocal Rank Fusion

A simple fusion mechanism is Reciprocal Rank Fusion:

\[
RRF(d) = \sum_i \frac{1}{k + rank_i(d)}
\]

The important engineering idea is not the formula itself. It is that heterogeneous retrievers can contribute evidence without pretending their raw scores are directly comparable.

### Graph traversal as evidence expansion

Suppose the user asks why a product is affected by an incident. A direct semantic match may retrieve the incident report but miss the causal chain:

```text
Incident
   ↓ AFFECTS
Product
   ↓ PRODUCED_BY
Supplier
   ↓ GOVERNED_BY
Contract
   ↓ SUBJECT_TO
Policy
```

A graph traversal can deliberately expose that path. The language model can then explain the path using grounded evidence rather than inventing relationships.

### Multi-hop limits

More hops are not automatically better. Each additional hop can increase noise and introduce provenance uncertainty. Set explicit traversal limits, relationship allowlists, and evidence thresholds. A good system can say:

> “The available evidence supports a two-hop relationship; the third hop depends on an unverified association.”

That is stronger than producing a confident four-hop story.

## 3. Evidence construction and answer grounding

The capstone should construct an evidence package rather than dumping search results into a prompt.

A useful evidence record contains:

```text
source_id
source_type
document_or_node_id
relevance_signal
provenance
observed_at
valid_from
valid_to
extraction_version
retrieval_method
```

The final model context should make it possible to trace important claims back to the evidence that supports them.

### Contradictory evidence

A realistic system will find contradictions:

- one system says a contract is active;
- another says it was terminated;
- a later document supersedes the earlier one;
- timestamps disagree;
- two extraction pipelines create conflicting graph edges.

Do not ask the model to casually “pick the truth.” Define deterministic precedence rules where possible, surface unresolved conflicts, and preserve both claims with provenance.

A useful final answer may therefore distinguish:

1. **Supported current facts**
2. **Historical facts**
3. **Conflicting evidence**
4. **Unknown or unverified claims**

## 4. The harness: the control plane around the model

The harness is the core differentiator between a demo agent and an engineered agent.

The harness should own responsibilities such as:

- state transitions;
- context assembly;
- tool availability;
- policy checks;
- budget accounting;
- retry limits;
- timeouts;
- checkpointing;
- cancellation;
- structured telemetry;
- verification calls;
- recovery behavior.

The model should not be the only authority for these controls.

### Deterministic boundary pattern

A robust loop resembles:

```text
observe state
   ↓
retrieve / inspect evidence
   ↓
model proposes next step
   ↓
validate proposal
   ↓
policy check
   ↓
budget check
   ↓
execute bounded action
   ↓
verify result
   ↓
commit state transition
   ↓
checkpoint + trace
   ↓
continue / pause / terminate
```

The important ordering is intentional. Do not commit a state transition before the action result is known when the transition asserts that the action succeeded.

### Budgeting

Budget should be multi-dimensional:

- wall-clock time;
- model calls;
- tool calls;
- retrieval calls;
- graph traversal depth;
- tokens or context size;
- monetary cost;
- action count.

A single “max iterations” value is usually too crude for a frontier agent.

## 5. Durable autonomy

Durable autonomy means that useful work survives process failure and can be resumed without losing the reasoning state needed for safe continuation.

### Checkpoints

A checkpoint should capture enough state to resume deterministically or at least safely. Depending on the architecture, this can include:

- task identifier;
- state version;
- current plan;
- completed steps;
- pending steps;
- evidence references;
- tool outcomes;
- approval status;
- budget remaining;
- leases or ownership metadata;
- artifact versions.

Avoid storing secrets simply because the checkpoint is convenient. Persistence expands the attack surface.

### Leases and heartbeats

For long-running work, the system must know whether a worker still owns the task. A lease with a heartbeat can prevent two workers from simultaneously believing they own the same execution.

The failure case matters more than the happy path:

```text
Worker A owns lease
      ↓
Worker A crashes
      ↓
heartbeat stops
      ↓
lease expires
      ↓
Worker B acquires lease
      ↓
resume from checkpoint
```

The recovery design must still address side effects that happened immediately before Worker A failed.

### Idempotency

A durable system must assume retries and replay.

For example, if an agent submits an external ticket and crashes before recording success, a retry may submit the same ticket again. The solution is not “tell the model not to retry.” The tool contract should expose an idempotency key or equivalent deduplication mechanism.

## 6. Computer use as a controlled execution surface

Computer use should enter the capstone only where the external interface is genuinely necessary. It adds capabilities but also introduces a new environment model.

The agent may need to reason from:

- screenshots;
- DOM or accessibility structure;
- current page state;
- selected application context;
- dialog state;
- transient UI information.

### Stale state

A screenshot or DOM snapshot is evidence about a point in time, not a perpetual truth.

Consider:

```text
observe page
   ↓
model chooses “Approve”
   ↓
page changes
   ↓
button moves / disappears
   ↓
blind click
```

The harness should re-check relevant state before a consequential action.

### Action tiers

A useful risk model distinguishes:

**Read-only:** navigation, inspection, searching.

**Reversible write:** editing a draft or changing a non-critical field.

**High-impact or irreversible:** financial approval, deletion, publication, external commitment.

The higher the action risk, the stronger the requirements for fresh state, deterministic policy, explicit confirmation, and independent verification.

### Human approval

Human approval is not a substitute for good engineering. It is a deliberately placed control boundary for actions where the residual risk is unacceptable for unattended execution.

The approval request should make the decision understandable:

- what will happen;
- why the agent proposes it;
- what evidence supports it;
- what policy authorizes it;
- what could go wrong.

## 7. Verification as an architectural layer

Verification should be independent enough to catch failures in the component that produced the proposal.

### Verification levels

**Retrieval verification:** Did required evidence enter the candidate set?

**Graph verification:** Are traversed relationships valid, typed, and temporally applicable?

**Plan verification:** Are preconditions satisfied? Are steps internally consistent?

**Tool verification:** Did the tool return a valid result? Did the expected side effect occur?

**Policy verification:** Was the action permitted for this identity, tenant, data class, and risk level?

**Outcome verification:** Does the final state satisfy the task’s acceptance criteria?

### Example

Suppose the agent proposes:

> “Disable Supplier A because it violated the active security requirement.”

A verifier should not merely ask another model whether this sentence sounds reasonable. It should check, where possible:

1. the supplier identity;
2. the exact requirement;
3. the policy version and effective dates;
4. the evidence of violation;
5. whether the violation is confirmed or only suspected;
6. whether the actor has authority to disable the supplier;
7. whether a required approval exists;
8. whether the external system actually reflects the intended state after execution.

## 8. Self-improvement without uncontrolled self-modification

A frontier agent should not be allowed to rewrite its own production behavior and immediately trust the result.

Use a candidate promotion pipeline:

```text
observed failure / opportunity
          ↓
 improvement hypothesis
          ↓
 candidate artifact
          ↓
 isolated evaluation
          ↓
 adversarial / failure tests
          ↓
 held-out evaluation
          ↓
 canary or shadow comparison
          ↓
 promotion gate
          ↓
 production
          ↓
 monitoring + rollback
```

### Candidate artifacts

Candidates may include:

- retrieval policies;
- ranking rules;
- prompts;
- tool routing policies;
- graph extraction rules;
- verifier thresholds;
- context assembly logic;
- workflow policies.

Each candidate should have a version and provenance.

### Improvement hypotheses

An improvement hypothesis should be falsifiable.

Weak:

> “Make the agent smarter.”

Strong:

> “Adding graph-path evidence for relationship-heavy queries will increase supported multi-hop answer rate without increasing unsupported-claim rate by more than the approved threshold.”

The second statement defines both a target and a safety constraint.

### Reward hacking and evaluator gaming

An optimizer can improve the measured score without improving the underlying task. For example:

- optimizing citation count rather than citation correctness;
- choosing easier queries;
- learning quirks of a particular evaluator;
- increasing refusal rates to avoid difficult cases;
- generating longer answers that appear more complete but contain more unsupported material.

The capstone should therefore use multiple evaluators, held-out tests, slice analysis, and adversarial cases rather than a single scalar score.

## 9. Evaluation strategy

The capstone needs an evaluation stack that measures both usefulness and safety.

### Retrieval metrics

Depending on the system and dataset, include:

- Recall@K;
- Precision@K;
- MRR or another ranking metric;
- graph-path hit rate;
- evidence coverage;
- temporal-validity accuracy.

### Generation metrics

Use task-appropriate measures such as:

- groundedness;
- citation correctness;
- answer completeness;
- unsupported-claim rate;
- contradiction rate.

### Agent metrics

Track:

- task success rate;
- successful completion without human intervention;
- unnecessary tool calls;
- verification failure rate;
- recovery success rate;
- termination correctness.

### Durable-operation metrics

Track:

- checkpoint recovery success;
- duplicate-side-effect rate;
- lease conflict rate;
- resume latency;
- abandoned task rate.

### Computer-use metrics

Track:

- successful environment grounding;
- stale-state detection rate;
- action verification success;
- blocked unsafe actions;
- human-approval escalation rate.

### Self-improvement metrics

Track both improvement and regression:

- delta in primary task metric;
- unsupported behavior delta;
- cost delta;
- latency delta;
- failure severity delta;
- rollback frequency.

A candidate should never be promoted because one metric improved while a critical safety metric regressed beyond its allowed threshold.

## 10. Failure-first test plan

A capstone is incomplete without deliberately breaking it.

### Retrieval failures

Inject:

- missing documents;
- duplicate documents;
- stale documents;
- conflicting records;
- incorrect metadata;
- graph edges with bad provenance;
- entity-resolution collisions.

Expected behavior should distinguish “not found” from “found but conflicting.”

### Agent-loop failures

Inject:

- repeated tool calls;
- invalid tool arguments;
- cyclic planning;
- budget exhaustion;
- malformed intermediate state;
- verifier rejection;
- cancellation.

The harness should terminate or recover according to an explicit policy rather than depending on the model to notice the problem.

### Durable-execution failures

Inject:

- process crash after checkpoint;
- crash before checkpoint;
- lease expiration;
- delayed heartbeat;
- duplicate worker;
- tool timeout;
- retry after ambiguous external result.

The key assertion is that recovery must preserve consistency and avoid unsafe duplicate side effects.

### Computer-use failures

Inject:

- DOM changes;
- stale screenshot;
- unexpected modal;
- changed account or tenant context;
- permission downgrade;
- partial action completion.

The system should detect when its observation is stale and re-ground before acting.

### Self-improvement failures

Inject:

- candidate that improves one benchmark while harming another;
- evaluator gaming;
- regression in rare slices;
- cost blow-up;
- prompt injection influencing candidate generation;
- verifier bypass attempt.

The promotion gate should reject these candidates.

## 11. Security model

The capstone combines many capabilities, so security must be compositional.

### Identity and tenant isolation

Authorization should be evaluated before sensitive retrieval and before high-impact action. Tenant filtering must apply before context construction, not merely after an answer is generated.

### Prompt injection

Documents, web pages, tickets, files, and application content are untrusted inputs. Retrieved text should not acquire tool authority simply because it appears in context.

Separate:

- **data** to be interpreted;
- **instructions** to be followed;
- **policy** to be enforced.

The harness should determine which instructions have authority.

### Tool security

Every tool should have:

- typed input validation;
- authorization;
- bounded scope;
- timeout;
- idempotency where applicable;
- audit logging;
- explicit error semantics.

### Graph poisoning

Graph ingestion can be attacked by introducing false entities or relationships. Treat extraction as proposal generation followed by validation. High-impact graph changes should be reviewable, provenance-backed, and reversible.

### Persistent-state risks

Long-lived memory and checkpoints can retain sensitive or stale information. Define retention, supersession, deletion, and access-control rules explicitly.

## 12. Observability and auditability

A frontier system must be explainable at the level of engineering evidence, not merely natural-language rationale.

A useful trace connects:

```text
request_id
  → retrieval calls
  → graph traversals
  → evidence set
  → model decisions
  → tool proposals
  → policy decisions
  → tool executions
  → state transitions
  → verifier results
  → final outcome
```

### What to record

Record enough to reproduce and diagnose behavior without indiscriminately storing secrets or raw sensitive content.

Useful fields include:

- request and task identifiers;
- actor and tenant identifiers where appropriate;
- model/version identifiers;
- retrieval configuration;
- graph schema/version;
- policy version;
- tool/version;
- checkpoint version;
- latency;
- token or cost attribution;
- verification outcome;
- final status.

### Trace interpretation

When an incident occurs, find the **first incorrect observable state**, not merely the last error message.

Example:

```text
retrieval correct
   ↓
graph path incorrect
   ↓
model explanation plausible
   ↓
plan based on wrong path
   ↓
verifier catches policy mismatch
```

The verifier prevented impact, but the root cause was earlier: graph-path construction.

## 13. Production-readiness gates

The capstone should not be declared complete because the demo works once.

A release candidate should satisfy gates for:

| Area | Example acceptance question |
|---|---|
| Retrieval | Does the system retrieve required evidence on the defined golden set? |
| Graph | Are critical relationships typed, provenance-backed, and temporally valid? |
| Grounding | Are important claims supported by traceable evidence? |
| Harness | Are budgets, retries, state transitions, and termination deterministic? |
| Durability | Can interrupted tasks resume without corrupting state or duplicating side effects? |
| Computer use | Are stale observations detected before high-impact actions? |
| Verification | Can invalid plans/actions/results be rejected independently? |
| Security | Are tenant, authorization, injection, and egress boundaries enforced? |
| Evaluation | Are critical slices and adversarial cases passing? |
| Operations | Can an engineer diagnose and roll back a bad release? |
| Cost | Is cost per successful task within the approved envelope? |

## 14. Worked scenario: investigation to governed action

Consider an investigation into a supplier-linked product incident.

### Step 1 — Interpret request

The system identifies the task as an investigation with possible operational impact. The risk gate determines that read access is allowed but any supplier suspension requires additional authority.

### Step 2 — Build candidate evidence

The retrieval plane searches:

- incident records;
- product documentation;
- supplier records;
- contracts;
- active policies;
- recent operational events.

Lexical retrieval catches exact identifiers. Vector search finds semantically related documents. Graph traversal connects incident → product → supplier → contract → policy.

### Step 3 — Resolve time

The system filters out superseded policies and distinguishes current from historical contractual state.

### Step 4 — Construct evidence graph

The system records which statements are supported and where conflicts remain.

### Step 5 — Plan

The model proposes:

1. confirm incident status;
2. identify affected products;
3. identify active supplier obligations;
4. check applicable policy;
5. prepare an operational recommendation.

The harness verifies preconditions and budget before each stage.

### Step 6 — Verify

A deterministic verifier checks that every high-impact recommendation has evidence, valid policy context, and authorized actor scope.

### Step 7 — Execute or escalate

For a low-risk action, the tool may execute. For a supplier suspension, the system requests human approval because the consequence is high-impact.

### Step 8 — Persist

The task checkpoint records the state and evidence references. After an interruption, the task resumes without repeating completed idempotent actions.

This scenario demonstrates why Module 43 is an integration capstone: no individual mechanism is enough.

## 15. Design principles to defend in a review

A strong capstone team should be able to defend these decisions:

### Why Graph-RAG instead of vector-only RAG?

Because some questions depend on explicit relationships, provenance, constraints, and multi-hop structure. The choice should be demonstrated with workload evidence, not fashion.

### Why hybrid retrieval instead of a single retriever?

Because exact identifiers, semantic descriptions, and relationship paths have different retrieval characteristics. Hybrid retrieval should earn its complexity through measurable gains.

### Why a harness instead of a model-only loop?

Because authorization, budgeting, state management, retries, checkpoints, and deterministic policy should not depend on probabilistic text generation.

### Why durable execution?

Because long-running tasks fail, workers restart, networks time out, and external side effects can become ambiguous. Durable state converts process failure into a recoverable condition.

### Why independent verification?

Because the component that proposes an action can be wrong. A verifier provides a separate acceptance boundary.

### Why controlled self-improvement?

Because autonomous optimization can exploit the evaluation system, degrade rare slices, increase cost, or bypass intended constraints. Promotion must therefore be evidence-based.

## 16. Exercises

### Exercise A — Build the minimal vertical slice

Implement one request end-to-end:

`request → hybrid retrieval → evidence package → model proposal → verification → final answer`

Use deterministic synthetic data first.

### Exercise B — Add graph reasoning

Construct a typed graph and answer a multi-hop question that vector retrieval alone cannot reliably answer.

### Exercise C — Inject contradiction

Create two conflicting source records with different effective dates. Make the system explain the conflict instead of silently choosing one.

### Exercise D — Make the task durable

Persist checkpoints and simulate a worker crash between two stages. Resume from state and prove that no duplicate side effect occurs.

### Exercise E — Add computer use

Introduce a synthetic browser or application environment. Change the UI between observation and action and verify that the agent refuses to act on stale state.

### Exercise F — Build a verifier

Create deterministic checks for authorization, required evidence, preconditions, and postconditions.

### Exercise G — Create a bad self-improvement candidate

Construct a candidate that improves one evaluation metric but harms another. Confirm that the promotion gate rejects it.

### Exercise H — Incident reconstruction

Given only a trace, identify the first incorrect state, root cause, failed containment boundary, and regression test that should be added.

## 17. Mastery challenge

The final challenge is to answer a high-impact, relationship-heavy request using the complete capstone stack.

The submission should include:

1. architecture diagram;
2. graph schema and provenance model;
3. retrieval routing strategy;
4. evidence-package format;
5. harness state machine;
6. checkpoint and recovery design;
7. tool contracts and authorization model;
8. computer-use safety boundary if used;
9. verification strategy;
10. evaluation dataset and metrics;
11. failure-injection report;
12. cost and latency measurements;
13. security/threat model;
14. rollout and rollback plan;
15. self-improvement promotion policy.

## 18. Final engineering perspective

Module 43 should leave the learner with a durable design instinct: **frontier capability does not come from removing controls; it comes from making capable systems more explicit, testable, and recoverable.**

Graph-RAG provides richer evidence structure. The harness turns model output into bounded decisions. Durable state turns transient execution into recoverable workflows. Computer use connects the agent to real environments. Verification turns confidence into acceptance criteria. Self-improvement turns observed failure into an experimental process rather than an uncontrolled rewrite.

The resulting system is not “an autonomous chatbot.” It is a governed computational system whose intelligence emerges from the interaction of retrieval, structured knowledge, probabilistic reasoning, deterministic controls, tools, state, environment feedback, verification, and evaluation.

The final standard is therefore not:

> “Can the agent complete the demo?”

It is:

> **“Can the system complete useful work, explain its evidence, respect its boundaries, survive failure, recover safely, prove its outcome, and improve only when the evidence supports the change?”**

That is the engineering bar for a frontier Graph-RAG agentic capstone.
