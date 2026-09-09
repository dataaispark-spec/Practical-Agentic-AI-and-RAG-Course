# Course Roadmap & Engineering Governance

**Repository:** `dataaispark-spec/Practical-Agentic-AI-and-RAG-Course`  
**Canonical branch:** `main`  
**Current curriculum:** **43 modules**  
**Last roadmap refresh:** 2026-09-09

This directory is the course's **governance layer**. It defines what is canonical, what evidence every module must provide, how notebooks are taught, how graph/frontier material fits the progression, and what QA can and cannot certify.

> **Core principle:** the course is an engineering apprenticeship, not a collection of framework demos. Every major mechanism should be understood, implemented, broken, debugged, measured, optimized, secured and defended.

## Start here

| File | Authority / purpose |
|---|---|
| [`CANONICAL-43-MODULE-MAP.md`](./CANONICAL-43-MODULE-MAP.md) | **Source of truth** for module numbering, names and canonical directories. |
| [`43-MODULE-COMPLETION-MANIFEST.md`](./43-MODULE-COMPLETION-MANIFEST.md) | **Definition of done** and repository-level completion contract. |
| [`COURSE-ENGINEERING-STANDARDS.md`](./COURSE-ENGINEERING-STANDARDS.md) | **Primary best-practices standard** for theory, architecture, labs, security, evaluation, deployment and learner evidence. |
| [`COLAB-PRACTICE-NOTEBOOK-STANDARD.md`](./COLAB-PRACTICE-NOTEBOOK-STANDARD.md) | **Notebook standard** for progressive, executable, failure-first Colab learning. |
| [`MODULE-DEEP-PRACTICE-IMPLEMENTATION-PACK.md`](./MODULE-DEEP-PRACTICE-IMPLEMENTATION-PACK.md) | Module-specific practice targets. Use as a companion to the canonical standards; it does not redefine the module map. |
| [`FRONTIER-AGENT-ENGINEERING.md`](./FRONTIER-AGENT-ENGINEERING.md) | Frontier engineering principles for Modules 36–43, including durable autonomy, harnesses, verifiers, self-improvement and computer use. |
| [`GRAPH-ENGINEERING-TRACK.md`](./GRAPH-ENGINEERING-TRACK.md) | Knowledge-graph / GraphRAG cross-cutting track for Modules 31–35 and later capstone integration. |
| [`GRAPH-ENGINEERING-QA.md`](./GRAPH-ENGINEERING-QA.md) | Graph-specific correctness and security contract. |
| [`course_qa_checker.py`](./course_qa_checker.py) | Machine-checkable structural/practice alignment QA for Modules 01–43. |
| [`module_objective_map.py`](./module_objective_map.py) | Explicit objective metadata consumed by QA and manual review. |
| [`43-MODULE-CONTENT-ALIGNMENT-AUDIT-2026-09-08.md`](./43-MODULE-CONTENT-ALIGNMENT-AUDIT-2026-09-08.md) | Dated audit evidence and remediation history. Historical record; not the normative standard. |
| [`M06-MERGE-REPORT.md`](./M06-MERGE-REPORT.md) | Dated Module 06 consolidation decision and compatibility/deprecation record. Historical record; not the normative standard. |
| [`RUNTIME-QA-STATUS-2026-09-08.md`](./RUNTIME-QA-STATUS-2026-09-08.md) | Dated runtime checkpoint. Historical evidence only; current certification must come from a fresh completed CI run. |

## Source-of-truth rules

1. **`main` is canonical.** New learner links, CI paths, notebooks and implementation references must target canonical paths on `main`.
2. **The 43-module map wins.** Older 38-module documents are historical/supporting material unless explicitly updated and relabeled.
3. **Module directories are authoritative.** README identity, notebook identity, application boundaries and tests must match the canonical module number.
4. **Legacy copies are not second modules.** Compatibility directories may remain temporarily, but no new learning content should be added there.
5. **Evidence beats claims.** File presence is not proof of pedagogical quality; notebook execution is not proof of semantic completeness; green structural QA is not proof of production readiness.
6. **No padding.** Do not inflate README/notebook length with repetitive prose, generic definitions, duplicated framework explanations or empty sections. Add depth only when it improves understanding, implementation, debugging, measurement or design judgment.
7. **Framework second, mechanism first.** Learners should see the underlying control/data/state mechanism before framework-specific abstractions.
8. **Provider-neutral core.** Core learning must remain runnable with deterministic/local fixtures where practical. Paid APIs and vendor services belong in optional extension cells or integration tests.

## Curriculum progression

```text
Know
  ↓
Retrieve
  ↓
Construct
  ↓
Connect
  ↓
Compound
  ↓
Reason
  ↓
Operate
  ↓
Persist
  ↓
Learn
  ↓
Improve
  ↓
Act
```

| Stage | Modules | Engineering emphasis |
|---|---|---|
| Foundations | 01–05 | systems thinking, Python, APIs, LLM application contracts, evaluation |
| RAG | 06–12 | ingestion, embeddings, retrieval, optimization, evaluation, debugging |
| Agent engineering | 13–18 | tools, loops, memory, state, planning, security |
| Distributed agents / MCP | 19–24 | multi-agent decision science, coordination, fault tolerance, MCP boundaries |
| Productionization | 25–30 | observability, production eval, economics, governance, deployment, capstone |
| Knowledge / graph | 31–35 | knowledge engineering, temporal graphs, agentic KG construction, hybrid retrieval, compounding knowledge |
| Frontier autonomy | 36–43 | loop engineering, harnesses, durable workers, continual skills/memory, environments/verifiers/RL, self-improvement, computer use, final capstone |

## Universal engineering model

For modules involving agentic behavior, use the following mental model:

```text
Agent System = Model + Harness + Environment + Tools + State + Policy + Verification + Evaluation
```

And reason through the control cycle:

```text
Observe → Decide → Act → Verify → Recover / Stop → Record
```

The model may propose a next action; deterministic controls must enforce boundaries such as schema validation, authorization, budgets, deadlines, state transitions, approval requirements, termination and audit.

## Required learner loop

Every substantive practical activity should follow:

```text
Predict → Build → Try → Observe → Break → Debug → Measure → Improve → Defend
```

The learner should not merely execute a notebook. They should be able to explain why the result happened, identify the invariant, diagnose a failure and defend a design choice.

## Module quality contract

Every canonical module should expose, either directly or through clearly linked companion material:

```text
Learning objectives
→ theory / mechanism
→ concept map
→ architecture + data/control flow
→ smallest runnable implementation
→ guided labs
→ independent exercise
→ intentional failure + debugging
→ measurement / evaluation
→ security / misuse analysis
→ production hardening + trade-offs
→ tests / assertions
→ interview + system design practice
→ mastery gate
→ next-module bridge + AegisAI integration
```

Not every concept needs the same amount of material. Depth should follow the mechanism's risk and complexity. A small concept can have a small notebook; a high-risk production concept should have explicit failure, measurement and security evidence.

## Cross-cutting best practices

### 1. Requirements before architecture

Start from users, constraints, data sensitivity, actionability, reliability targets, latency, cost and operational ownership. Prefer the minimum architecture that satisfies the requirements. Do not introduce agents or multi-agent orchestration merely because the topic is “agentic AI.”

### 2. Separate data plane from control plane

Untrusted documents, retrieved passages, tool outputs, memory entries and observations are **data**, not authority. Policy, identity, authorization, budgets, approvals and state-transition rules belong to the control plane and must not be overridden by model-generated text.

### 3. Make state explicit

Name the state, ownership, lifetime and recovery semantics. Distinguish ephemeral context from durable state; authoritative state from advisory memory; desired state from observed state. A restart should have a defined outcome rather than accidental behavior.

### 4. Treat every boundary as a contract

Use typed schemas, input validation, output validation, versioned envelopes and explicit error classes for APIs, tools, agent messages, graph records, checkpoints and evaluation results.

### 5. Design failure before scale

Every module should intentionally inject at least one relevant failure. Agent/RAG/production modules should normally test multiple classes such as malformed input, dependency failure, timeout, stale data/state, authorization failure, poisoned context, retry amplification, misleading success and resource exhaustion.

### 6. Make actions idempotent and replayable

Where a retry can produce a side effect, define an idempotency key or equivalent action identity. Capture enough structured trajectory/trace data to reconstruct what the system believed, attempted and observed.

### 7. Verify independently

Do not let an agent certify its own success when a stronger verifier is feasible. Verification should check task-specific postconditions, invariants or external evidence. “The model said it succeeded” is not a sufficient verification signal for consequential work.

### 8. Bound autonomy

Use explicit limits for steps, tokens/context, tool calls, time, monetary cost, concurrency, retries, recursion depth and high-risk actions. Add cancellation, deadlines and safe stopping behavior.

### 9. Evaluate slices, not just averages

Report task success and quality metrics with meaningful slices such as document type, tenant, difficulty, failure class, latency band or risk class where appropriate. Preserve a regression set. Explain measurement uncertainty and known blind spots.

### 10. Optimize against a multi-objective frontier

Quality, safety, latency, reliability and cost trade off. Measure cost per successful/verified task rather than token spend alone, and avoid “cheaper” routes that violate capability or policy constraints.

### 11. Secure persistence and learning

Memory, skills, graph updates, prompts, tools and self-improvement artifacts can become durable attack surfaces. Require provenance, validation, promotion gates, versioning, rollback and explicit trust transitions.

### 12. Release the whole AI system, not only application code

A reproducible release should identify the relevant application, model/provider, prompt/template, retrieval/index/embedding version, tool/MCP contract, policy configuration, evaluation set/version and deployment artifact. Shadow/canary/rollback should be possible for material changes.

### 13. Keep educational infrastructure deterministic

For the baseline path, prefer synthetic/local data, fake providers, mock tools and deterministic fixtures. External integrations should be optional and separately classified. CI should not depend on rate-limited third-party services for fundamental course mechanics.

### 14. Teach trade-offs and when *not* to use the technology

Every major module should include at least one negative case: when the architecture is unnecessary, too expensive, too risky, too slow or too difficult to operate. “Use X because X is modern” is not an architecture argument.

### 15. Separate stable principles from changing product facts

For frontier content, distinguish durable engineering ideas from current framework/product behavior, experimental research, vendor benchmark claims and learner-generated measurements. Re-check fast-changing product details against current authoritative documentation before teaching them as facts.

## Security baseline

Across the course, security is not a single module-only concern. Relevant modules should explicitly consider:

- identity and tenant binding;
- authentication and authorization;
- least privilege and capability allowlists;
- prompt injection and indirect instruction attacks;
- malicious tool/MCP outputs;
- memory/skill/graph poisoning;
- secret handling and egress controls;
- confused-deputy behavior;
- replay and duplicate side effects;
- stale approvals and revoked permissions;
- auditability and incident reconstruction;
- data minimization and provenance;
- consequential-action verification.

For high-risk educational scenarios, use synthetic data and simulated side effects.

## Assessment philosophy

A strong mastery gate should test more than recall:

| Level | Evidence |
|---|---|
| L1 | Explain the concept and assumptions. |
| L2 | Implement the smallest correct mechanism. |
| L3 | Diagnose an intentionally broken implementation. |
| L4 | Measure behavior and improve it. |
| L5 | Design a production architecture under constraints. |
| L6 | Defend trade-offs with evidence. |
| L7 | Solve a novel scenario without copying the guided solution. |

Use a mixture of conceptual questions, coding, debugging, measurement, system design and oral/written defense.

## AegisAI continuity

The course uses **AegisAI** as the single evolving capstone. Each module should answer:

1. What primitive does this module add to AegisAI?
2. Which earlier primitive does it depend on?
3. What new failure mode or systems constraint does it introduce?
4. What evidence should the learner carry into the next module?

Later modules should extend the system rather than repeatedly rebuilding unrelated toy projects.

## QA and certification rules

The repository should treat QA as layered evidence:

```text
Structural QA
   ↓
Module tests
   ↓
Clean-kernel notebook runtime
   ↓
Aggregate CI gate
   ↓
Manual semantic review
   ↓
Course certification
```

Automated checks can prove file shape, importability, assertions and runtime behavior. They cannot by themselves prove that a tutorial is well explained, pedagogically coherent or production-realistic.

The course is **not QA-certified** until the current GitHub Actions workflow completes successfully across the required checks. Queued, running, partial or stale runs do not count.

## Change-control policy for this roadmap

When adding or revising a module:

1. Update the canonical module map if identity or sequence changes.
2. Update objective metadata and the completion manifest when scope changes.
3. Update notebook/app/test standards only when the rule itself changes; do not copy standards into every module.
4. Record dated audits as evidence, not as competing definitions of the standard.
5. Fix underlying invariants rather than weakening QA to obtain green CI.
6. After material changes, run structural QA, relevant tests, notebook runtime and the full aggregate workflow before declaring certification.

## Definition of quality

A course artifact is worth keeping when it makes the learner **more capable of building, breaking, debugging, measuring, securing, operating or defending an AI system**. Content that does not serve that goal should be shortened, merged or removed.
