# Module 34 — Graph + Vector Hybrid Retrieval

**Canonical implementation:** `34-graph-vector-hybrid-retrieval/`

**Course position:** Graph Engineering Track — Module 34 of 43

**Previous:** Module 33 — Agentic Knowledge Graph Construction  
**Next:** Module 35 — Compounding Knowledge / LLM Wiki

> **Core thesis:** Graph and vector retrieval provide different signals. Hybrid retrieval is justified only when controlled experiments show a meaningful quality gain that survives security, latency, cost and maintenance constraints.

## 1. Why this module exists

Vector search is excellent at semantic similarity. Graph retrieval is excellent at explicit identity and relationship constraints. Real enterprise workloads often need both.

```text
                         QUERY
                           |
              +------------+------------+
              |                         |
              v                         v
        VECTOR RETRIEVER          GRAPH RETRIEVER
              |                         |
        dense candidates          entities / paths
              |                         |
              +------------+------------+
                           v
                     candidate union
                           |
                 tenant / ACL / time
                           |
                       RRF fusion
                           |
                       reranker
                           |
                  bounded evidence
                           |
                      verifier
                           |
                         answer
```

## 2. Learning outcomes

You will be able to:

1. explain strengths and failure modes of vector and graph retrieval;
2. implement graph-only and vector-only baselines;
3. construct candidate unions and reciprocal-rank fusion;
4. apply security and temporal filters before candidate truncation;
5. add graph/path/freshness signals to ranking;
6. add a reranking stage and analyze its cost;
7. design multi-hop retrieval datasets;
8. evaluate Recall@K, MRR, nDCG and path accuracy;
9. measure p50/p95 latency, traversal work, tokens and cost;
10. decompose retrieval errors into vector, graph, fusion, reranker and generation failures;
11. prevent graph poisoning and unauthorized candidates from reaching context;
12. write an architecture decision record defending or rejecting hybrid retrieval.

## 3. Component architecture

| Component | Purpose | Failure prevented |
|---|---|---|
| Vector retriever | semantic candidate recall | concept mismatch |
| Graph retriever | explicit path/entity recall | multi-hop miss |
| Candidate normalizer | common IDs/scores | duplicate candidates |
| Access filter | tenant/ACL scope | data leakage |
| Temporal filter | current/historical validity | stale evidence |
| Fusion | combine ranking signals | single-source blind spots |
| Reranker | fine relevance judgment | noisy top-k |
| Evidence assembler | preserve provenance | unsupported answer |
| Verifier | validate answer support | false completion |
| Benchmark harness | controlled comparison | architecture guesswork |

## 4. Theory / deep dive

Read [`theory/GRAPH-VECTOR-HYBRID-RETRIEVAL-THEORY.md`](theory/GRAPH-VECTOR-HYBRID-RETRIEVAL-THEORY.md).

Topics include vector and graph retrieval mechanics, hybrid patterns, RRF, reranking, multi-hop evaluation, error decomposition, production economics and security ordering.

## 5. Hands-on labs

1. **BUILD:** one benchmark corpus and labeled question set.
2. **BUILD:** vector retrieval baseline.
3. **BUILD:** bounded graph retrieval baseline.
4. **TRY:** candidate union.
5. **TRY:** reciprocal-rank fusion.
6. **TRY:** graph-aware reranking.
7. **BREAK:** graph miss.
8. **BREAK:** vector miss.
9. **BREAK:** duplicate entity candidates.
10. **BREAK:** contradictory evidence.
11. **BREAK:** poisoned subgraph.
12. **BREAK:** candidate truncation before authorization.
13. **BREAK:** traversal explosion.
14. **MEASURE:** Recall@K, MRR, nDCG, multi-hop accuracy.
15. **MEASURE:** p50/p95 latency, traversal work, token use and cost.
16. **IMPROVE:** tune fusion/reranking under a fixed evaluation set.
17. **DEFEND:** write an ADR with evidence for/against hybrid adoption.

## 6. Domain-specific tracks

### Cybersecurity
Query `Asset → Vulnerability → Control → Owner` while vector search finds advisory passages. Exercise: retrieve the correct remediation owner and prove the path.

### Banking
Combine transaction-policy text with `Customer → Account → Transaction → Case` graph paths. Exercise: answer a fraud-investigation question without using evidence outside the authorized customer scope.

### Healthcare
Use semantic literature retrieval plus `Drug → Condition → Guideline` paths. Exercise: distinguish “related literature” from an explicit guideline relationship and preserve provenance.

### Manufacturing
Combine maintenance text with `Machine → Component → FailureMode → WorkOrder`. Exercise: identify the most likely maintenance action from both semantic and structural evidence.

### Enterprise IT
Combine incident/runbook vectors with `Service → Dependency → Team → Incident` graph paths. Exercise: diagnose a service dependency outage and cite the supporting path.

## 7. Benchmark protocol

Hold constant:

- corpus version;
- query set and labels;
- tenant/ACL policy;
- answer/evaluation budget;
- evaluator;
- infrastructure as far as practical.

Compare:

```text
A. vector-only
B. graph-only
C. union
D. RRF
E. hybrid + reranker
```

Do not report only final answer quality. Report retrieval and operational metrics separately.

## 8. Retrieval debugging matrix

| Symptom | Likely layer | First evidence |
|---|---|---|
| semantic answer missing | vector | candidate recall |
| path incomplete | graph | edge/path validity |
| good candidates ranked low | fusion | rank contribution |
| top result irrelevant | reranker | candidate labels |
| right evidence, wrong answer | generation | context/provenance |
| answer cites stale policy | temporal/cache | validity + version |
| unauthorized source appears | security | filter ordering |

## 9. Failure contract

For every fault capture:

**symptom → evidence → hypothesis → controlled experiment → root cause → fix → regression test → residual risk**.

## 10. Measurements

Minimum scorecard:

- Recall@K;
- MRR;
- nDCG;
- multi-hop/path accuracy;
- groundedness/provenance coverage;
- candidate count;
- traversal nodes/edges;
- p50/p95 latency;
- tokens/request;
- cost/success;
- unsafe candidate rate;
- regression delta versus baseline.

## 11. Coding challenges

1. Implement RRF from scratch.
2. Add score normalization and compare it with rank fusion.
3. Implement a path-aware reranker.
4. Add temporal and ACL filtering before truncation.
5. Build a retrieval-error decomposition report.
6. Add benchmark regression thresholds.
7. Create adversarial tests for poisoned graph candidates.

## 12. System-design challenge

Design hybrid retrieval for **100M documents + 100M entities**. Defend indexing, candidate fan-out, graph partitioning, cache strategy, authorization order, reranking, latency budgets, evaluation, cost and failure recovery.

## 13. Interview bank

### Advanced
- Why can graph retrieval improve multi-hop recall but reduce overall answer quality?
- What is RRF and when is it preferable to score fusion?
- Why must ACL filtering happen before top-k truncation?

### Senior/Staff
- How would you prove that hybrid retrieval is worth its operational complexity?
- Design a multi-tenant hybrid retrieval system with p95 < 500 ms.
- How would you diagnose a 10-point Recall@10 regression after a graph update?

## 14. GitHub deliverables

```text
34-graph-vector-hybrid-retrieval/
├── README.md
├── EXERCISES.md
├── theory/GRAPH-VECTOR-HYBRID-RETRIEVAL-THEORY.md
├── app/
├── notebooks/module_34_graph_vector_hybrid_retrieval.ipynb
└── tests/
```

## 15. Mastery gate

Build all major retrieval baselines, run the controlled benchmark, explain quality/latency/cost trade-offs, inject security and retrieval failures, and defend a production architecture decision with measured evidence.

**Handoff:** M34 optimizes evidence retrieval. M35 turns validated evidence into durable, compounding organizational knowledge.