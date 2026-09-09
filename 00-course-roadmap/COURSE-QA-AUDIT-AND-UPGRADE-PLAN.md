# Course QA & Content-Quality Plan — Superseded Historical Audit

**Audit scope:** the 43-module canonical curriculum on `main`  
**Historical checkpoint:** 2026-09-08/09  
**Status:** **historical evidence, not the normative course standard**

> The authoritative governance documents are now [`README.md`](./README.md), [`CANONICAL-43-MODULE-MAP.md`](./CANONICAL-43-MODULE-MAP.md), [`43-MODULE-COMPLETION-MANIFEST.md`](./43-MODULE-COMPLETION-MANIFEST.md), [`COURSE-ENGINEERING-STANDARDS.md`](./COURSE-ENGINEERING-STANDARDS.md) and [`COLAB-PRACTICE-NOTEBOOK-STANDARD.md`](./COLAB-PRACTICE-NOTEBOOK-STANDARD.md).

## Why this file is retained

This document records an earlier broad QA/audit pass and the kinds of evidence that were being requested at that point. It is retained for auditability; it must not be copied as a second set of current rules.

The central finding remains important:

> **A module having a README, app, tests and notebook does not by itself prove a complete practical learning experience.**

Quality depends on the learner being able to understand the mechanism, implement it, break it, debug it, measure it, secure it, optimize it and defend it.

## Historical learning loop

```text
Theory
→ Architecture
→ Worked example
→ Runnable implementation
→ Guided practice
→ Independent challenge
→ Failure / debugging
→ Measurement
→ Industry scenario
→ Production hardening
→ Solution / reference implementation
→ Interview / system design
→ Mastery
```

This is consistent with the current engineering and Colab standards; the current files should be used for exact acceptance criteria.

## Historical focus areas

- Foundations: architecture decisions, Python reliability, API contracts, LLM application boundaries and prompt evaluation.
- RAG: first-principles retrieval, embedding/vector systems, document intelligence/PII, hybrid retrieval, optimization, evaluation and debugging.
- Agents: tools, raw loops, memory, stateful workflows, planning/HITL and security.
- Distributed systems: multi-agent decision science, architectures, coordination/fault tolerance, debugging and MCP.
- Production: observability, production evaluation, cost, governance, deployment and the first AegisAI capstone.
- Knowledge/frontier: knowledge graphs, temporal knowledge, graph/vector retrieval, compounding knowledge, loop/harness engineering, durable autonomy, continual skills/memory, verifiers/RL, recursive improvement, computer use and the final capstone.

## Historical cleanup notes

### Canonical Module 06

The consolidation decision is recorded in [`M06-MERGE-REPORT.md`](./M06-MERGE-REPORT.md): `06-rag-from-first-principles/` is canonical. Legacy `06-rag-first-principles/` content is not a second module.

### Canonical frontier numbering

The 43-module map is authoritative. Historical former `31–38` frontier paths are compatibility copies only. New links and learner-facing references must use canonical `31–43` paths.

### Runtime evidence

[`RUNTIME-QA-STATUS-2026-09-08.md`](./RUNTIME-QA-STATUS-2026-09-08.md) records a prior checkpoint. It explicitly did **not** claim full QA certification. A current green claim requires a fresh completed CI run.

## Review discipline

Use the current standards to evaluate new changes. In particular:

- do not weaken QA rules simply to make CI green;
- do not equate file count with instructional quality;
- do not pad READMEs/notebooks with repetitive text;
- do not treat external vendor behavior as a stable engineering principle;
- do not require paid APIs for the core educational path;
- do not let model output bypass deterministic control-plane constraints;
- do not certify a module on runtime evidence alone without manual semantic review.
