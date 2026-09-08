# Graph Engineering QA Contract

This contract extends the existing structural/runtime QA with graph-specific correctness checks.

## Required graph evidence

- [ ] typed entity/relation/claim schema
- [ ] provenance required for trusted edges
- [ ] tenant/ACL filtering before graph traversal results reach the model
- [ ] bounded hop/node traversal
- [ ] deterministic entity-resolution behavior
- [ ] contradiction and supersession handling
- [ ] temporal validity (`valid_from` / `valid_to`) where the scenario needs it
- [ ] graph poisoning test
- [ ] vector-vs-graph-vs-hybrid comparison
- [ ] graph health metrics
- [ ] rollback/recovery for bad knowledge updates
- [ ] ADR documenting when graph is unnecessary

## Failure-contract format

Every graph failure lab should record:

```text
FAILURE-ID
setup
injected fault
expected observable
expected failure class
expected recovery
regression assertion
```

## Security gate

A graph-derived recommendation must never directly authorize an external action. The action still passes identity, authorization, policy, budget, approval (when required), verification and audit controls.

## CI principle

Core graph tests must run with deterministic/local dependencies. Vendor graph databases and external LLMs are optional integration tests and must not make the educational baseline flaky.

## Current implementation anchors

- `00-course-toolkit/graph/` — shared graph primitives
- `31-loop-engineering/app/graph_observation.py` — graph-aware loop observations
- `32-harness-engineering/app/graph_rag.py` — bounded GraphRAG + RRF primitive
- `33-long-running-autonomous-agents/app/compounding_knowledge.py` — maintained knowledge updates
- `31-loop-engineering/notebooks/module_31_graph_engineering_extension.ipynb`
- `32-harness-engineering/notebooks/module_32_graphrag_extension.ipynb`
- `33-long-running-autonomous-agents/notebooks/module_33_compounding_knowledge_extension.ipynb`
