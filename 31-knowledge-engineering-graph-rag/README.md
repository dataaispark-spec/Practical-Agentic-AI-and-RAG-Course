# Module 31 — Knowledge Engineering & Graph RAG

## Purpose

Move from unstructured retrieval to explicit, inspectable knowledge. Build a vendor-neutral GraphRAG baseline and learn when graph structure adds value over vector retrieval.

## Learning outcomes

- design a small ontology/schema;
- represent entities, relations, claims and evidence;
- preserve tenant, ACL and provenance boundaries;
- build bounded neighborhood retrieval;
- compare vector-only, graph-only and hybrid retrieval;
- measure multi-hop accuracy, Recall@K, MRR, groundedness, latency and cost;
- explain when **not** to use a knowledge graph.

## Mechanism

```text
sources → entities/claims → relations → validated graph
                                      ↓
                         bounded graph retrieval
                                      ↓
                        graph + vector evidence
                                      ↓
                              agent / verifier
```

## Labs

1. Define ontology and entity types.
2. Build deterministic entities and edges.
3. Attach claims and source provenance.
4. Implement bounded traversal.
5. Add tenant/ACL filtering before traversal.
6. Construct multi-hop questions.
7. Benchmark vector vs graph vs hybrid retrieval.
8. Inject duplicate entities and hallucinated edges.
9. Detect poisoned evidence.
10. Produce a graph-health report.

## Failure-first cases

Duplicate entity, wrong relation direction, missing provenance, unbounded traversal, tenant leakage, poisoned edge and graph-to-agent escalation.

## Colab

`notebooks/module_31_knowledge_engineering_graph_rag.ipynb` is executable without API keys and uses deterministic data so the learner can focus on mechanism and measurement.

## Production rule

A graph is **evidence, not authority**. Authorization, policy, budgets, verification and audit remain outside the graph.
