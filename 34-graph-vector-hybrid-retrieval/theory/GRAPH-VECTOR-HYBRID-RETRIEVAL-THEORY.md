# Module 34 — Graph + Vector Hybrid Retrieval: Theory and Benchmarking

## 1. Mission

Module 34 teaches a critical production discipline: **do not adopt GraphRAG because it is fashionable; prove that the graph signal improves the target task enough to justify its latency, complexity and maintenance cost.**

The module compares vector-only, graph-only, fused and reranked retrieval under the same corpus, questions and evaluation set.

## 2. Retrieval architecture

```text
                         QUERY
                           |
                +----------+----------+
                |                     |
                v                     v
          vector retrieval       graph retrieval
                |                     |
           dense scores         paths / entities
                |                     |
                +----------+----------+
                           v
                    candidate union
                           |
                   ACL / tenant filter
                           |
                    temporal filter
                           |
                    rank fusion
                           |
                       reranker
                           |
                 bounded evidence set
                           |
                       verifier
                           |
                        answer
```

Security filters must occur before a candidate can influence ranking or context. Filtering after truncation can accidentally remove authorized evidence while leaving unauthorized candidates in the top-k set.

## 3. Vector retrieval strengths

Dense retrieval is strong when semantic similarity is the dominant signal. It is simple, mature and often cheaper to operate.

Failure modes:

- entity ambiguity;
- multi-hop relationship questions;
- exact identifiers with weak semantic neighborhoods;
- contradictory documents;
- relationship direction not represented in embeddings.

## 4. Graph retrieval strengths

Graph retrieval is strong when the query depends on explicit relationships and constrained paths.

Failure modes:

- incomplete graph construction;
- stale edges;
- wrong entity resolution;
- traversal explosion;
- poor coverage for concepts absent from the graph.

## 5. Hybrid retrieval

Hybrid retrieval exploits complementary evidence.

Three common patterns:

### Candidate union
Retrieve top-N from both systems and merge.

### Constraint-aware retrieval
Use graph relationships to constrain vector candidates.

### Feature fusion
Combine vector score, graph path score, freshness, source authority and other signals.

The learner should implement at least one simple fusion method and then compare it experimentally.

## 6. Reciprocal Rank Fusion

For result rank `r`, a simple RRF contribution is:

```text
score(d) += 1 / (k + r)
```

where `k` is a smoothing constant. RRF is attractive because it combines rankings without requiring score calibration across systems.

It is not magic: duplicate entities, unauthorized candidates and poor candidate sets can still produce bad results.

## 7. Reranking

A reranker receives a smaller candidate set and estimates query-document relevance more carefully.

```text
1000 candidates
      |
   filters
      |
   top 100
      |
   reranker
      |
    top 10
```

Teach the latency/quality trade-off and the risk of optimizing on a narrow evaluation set.

## 8. Multi-hop retrieval

Create questions whose answer depends on a path:

```text
Customer → Contract → Product → Dependency → Owner
```

The benchmark must distinguish:

- retrieved the right documents;
- found the right entities;
- found a valid path;
- produced a grounded final answer.

A single final-answer score hides these failure locations.

## 9. Evaluation protocol

Hold constant:

- corpus version;
- query set;
- relevance labels;
- evaluator;
- tenant/ACL policy;
- answer budget;
- hardware/environment where possible.

Compare:

1. vector-only;
2. graph-only;
3. vector + graph union;
4. RRF;
5. hybrid + reranker.

Metrics:

- Recall@K;
- MRR;
- nDCG;
- hit rate;
- multi-hop path accuracy;
- groundedness/provenance coverage;
- p50/p95 latency;
- candidate count;
- traversal work;
- token count;
- cost per successful task.

## 10. Retrieval error decomposition

```text
Poor answer
   |
   +--> retrieval miss?
   |       |
   |       +--> vector miss
   |       +--> graph miss
   |
   +--> fusion error?
   |
   +--> reranker error?
   |
   +--> context assembly error?
   |
   +--> generation/verifier error?
```

This decomposition is essential for meaningful debugging.

## 11. Failure-first labs

Break one variable at a time:

- remove graph edges;
- remove vector candidates;
- inject a poisoned subgraph;
- truncate before ACL filtering;
- create duplicate entities;
- add contradictory sources;
- increase traversal depth until budget failure;
- over-rerank with a biased scoring rule;
- evaluate on questions not represented in the graph.

Record **symptom → evidence → hypothesis → experiment → root cause → fix → regression test**.

## 12. Production decision economics

Hybrid architecture adds:

- graph construction and maintenance;
- additional storage/indexing;
- query planning;
- traversal latency;
- evaluation complexity;
- operational ownership.

The decision should therefore be expressed as:

```text
Incremental task-value gain
            /
Incremental operational cost
```

Adopt hybrid only when the measured gain is meaningful for the business SLO.

## 13. Security

Retrieval is a data-access boundary. Apply identity, tenant, ACL, freshness and policy constraints before candidate ranking/truncation and before context assembly. Graph structure must never grant authorization.

## 14. Handoff to Module 35

Module 34 optimizes retrieval of current evidence. Module 35 moves upward into **compounding knowledge**: validated claims, durable pages, contradiction handling, rollback and organizational learning.
