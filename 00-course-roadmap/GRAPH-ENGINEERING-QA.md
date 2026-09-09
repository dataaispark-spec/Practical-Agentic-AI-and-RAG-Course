# Graph Engineering QA Contract

**Status:** normative extension to the course engineering and QA standards  
**Scope:** Modules 31–35 and any later module using knowledge graphs / GraphRAG  
**Updated:** 2026-09-09

The general rules are in [`COURSE-ENGINEERING-STANDARDS.md`](./COURSE-ENGINEERING-STANDARDS.md). This file adds graph-specific correctness requirements.

## Required graph evidence

- [ ] typed entity / relation / claim schema;
- [ ] provenance attached to trusted knowledge;
- [ ] tenant / ACL filtering before graph evidence reaches the model;
- [ ] bounded hop/node traversal;
- [ ] deterministic entity-resolution behavior for the educational baseline;
- [ ] contradiction and supersession handling;
- [ ] temporal validity (`valid_from` / `valid_to`) where the use case needs history;
- [ ] graph poisoning test;
- [ ] vector-only vs graph-only vs hybrid comparison where applicable;
- [ ] graph health metrics;
- [ ] rollback / recovery for bad knowledge updates;
- [ ] an ADR documenting when a graph is unnecessary.

## Knowledge integrity contract

A graph record is not trustworthy merely because it exists. For claims/relations intended for reasoning, preserve enough metadata to answer:

```text
Who/what produced this claim?
Which source supports it?
When is it valid?
Which tenant / ACL applies?
What schema/version produced it?
Was it validated or merely proposed?
Has it been superseded or contradicted?
```

## Failure-contract format

Every graph failure lab should record:

```text
FAILURE-ID
setup
injected fault
violated invariant
expected observable
expected failure class
diagnosis
expected recovery
regression assertion
```

## Security gate

A graph-derived recommendation must never directly authorize an external action. The action still passes identity, authorization, policy, budget, approval when required, verification and audit controls.

Graph security includes storage security **and** relationship integrity, provenance integrity, inference boundaries and action authorization.

## CI principle

Core graph exercises and tests should run with deterministic/local dependencies. Vendor graph databases and external model calls belong in optional integration tests and must not make the educational baseline flaky.

## Benchmark standard

Where graph retrieval is a learning objective, compare equivalent query sets across:

1. vector-only;
2. graph-only;
3. graph + vector;
4. graph + vector + reranking / verification when relevant.

Measure task-relevant quality plus latency/cost/maintenance impact. Record cases where graph complexity makes the result worse.

## Canonical implementation anchors

Use the canonical numbered directories on `main`. Legacy compatibility paths must not be introduced into new learner-facing links.
