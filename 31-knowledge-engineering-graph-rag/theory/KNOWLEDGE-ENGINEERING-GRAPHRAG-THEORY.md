# Module 31 — Knowledge Engineering & Graph RAG: Theory and Architecture

## 1. Mission

Module 31 changes the learner's mental model from **documents that resemble knowledge** to **explicit knowledge that can be inspected, traversed, cited and evaluated**.

A graph is useful when the question depends on entities and relationships rather than only lexical or semantic similarity. It is not automatically better than vector retrieval.

```text
Documents / APIs / tickets / tables
                |
                v
       Evidence + provenance
                |
                v
       Entity / relation extraction
                |
                v
          Ontology / schema
                |
                v
      Validated knowledge graph
          /              \
         v                v
 bounded traversal    graph signals
         |                |
         +-------+--------+
                 v
        evidence assembly
                 |
                 v
          RAG / agent / verifier
```

## 2. Knowledge representation layers

### Evidence
The original source observation: document ID, passage, API response, timestamp, tenant, ACL and source authority.

### Entity
A stable identity such as `Customer:123`, `Supplier:Acme`, `System:Payments`.

### Relation
A typed connection such as `SUPPLIES`, `OWNS`, `DEPENDS_ON`, `REPORTS_TO`.

### Claim
A proposition that can be evaluated: subject + predicate + object/value + evidence + temporal scope + confidence.

### Graph projection
A queryable representation of validated claims. It is a derived knowledge structure, not an authorization system.

## 3. Ontology engineering

An ontology is a controlled vocabulary and set of relationship semantics. Teach learners to define:

- entity types;
- relation types and direction;
- cardinality;
- required attributes;
- identity keys and aliases;
- provenance requirements;
- temporal fields;
- tenant/ACL fields;
- schema version;
- deprecation rules.

A good ontology is intentionally small at first. Over-modeling creates maintenance cost and false precision.

### Schema example

```text
Supplier
  id, legal_name, country

Contract
  id, start_date, end_date, status

System
  id, owner_team, criticality

Supplier -[HAS_CONTRACT]-> Contract
Contract -[GOVERNS]-> System
System -[DEPENDS_ON]-> System
```

## 4. Entity identity is harder than extraction

Two strings can represent one entity; one string can represent several entities.

```text
"IBM"
"International Business Machines"
"IBM Corp."
```

Do not silently merge them. Resolve identity using deterministic keys, aliases, contextual attributes and confidence thresholds. Low-confidence resolution should enter review/quarantine.

Important metrics:

- precision of merges;
- false merge rate;
- false split rate;
- unresolved entity rate.

## 5. Relationship semantics

Direction matters. `A DEPENDS_ON B` is not equivalent to `B DEPENDS_ON A`.

Every edge should carry enough information to answer:

1. What is connected?
2. Why do we believe it?
3. Who/what supplied the evidence?
4. When was it true?
5. Which tenant can see it?
6. What schema version defined the relation?

## 6. Bounded graph retrieval

Graph traversal must have explicit limits.

```text
query entity
   |
   +--> hop 1
   |      |
   |      +--> hop 2
   |             |
   |             +--> hop 3
   |
   +--> max nodes / max edges / time budget
```

Controls include maximum hops, node/edge budget, relation allow-list, tenant filter, ACL filter, freshness policy and cycle detection.

Unbounded traversal is both a performance and security failure: a highly connected node can turn a targeted question into a graph-wide data exposure.

## 7. Graph RAG patterns

### Local GraphRAG
Retrieve a small neighborhood around a known entity.

### Global GraphRAG
Aggregate community/topic-level information. Useful for corpus-wide questions but more expensive and harder to evaluate.

### Hybrid Graph + Vector
Use semantic retrieval to locate candidate evidence and graph traversal to connect entities/relationships, or use graph structure to constrain vector candidates.

### Graph-aware reranking
Add structural signals such as path relevance, relation type, evidence freshness and source authority to ranking.

## 8. Multi-hop reasoning

A multi-hop question requires multiple supported edges.

Example:

```text
Supplier A
   |
   +--HAS_CONTRACT--> C1
                         |
                         +--GOVERNS--> Payment API
                                           |
                                           +--DEPENDS_ON--> Identity API
```

Question: *Which identity system is indirectly required by Supplier A's payment contract?*

A correct answer requires path preservation. A vector retriever may retrieve each concept independently without proving the connection.

## 9. Graph versus vector decision framework

Choose graph retrieval when:

- explicit relationships are central;
- multi-hop paths matter;
- entity identity is stable;
- relationship constraints improve precision;
- explainable paths are valuable.

Prefer vector retrieval when:

- the task is primarily semantic similarity;
- relationships are weak or unstable;
- graph maintenance cost exceeds measured value.

Use hybrid when the benchmark shows complementary recall/precision benefits.

## 10. Evidence assembly

The graph should return **evidence paths**, not just a prose answer.

```text
Answer candidate
   |
   +-- entity IDs
   +-- relation IDs
   +-- claim IDs
   +-- source passages
   +-- timestamps
   +-- confidence
   +-- tenant / ACL proof
```

The generator should not be allowed to invent missing edges.

## 11. Graph health

Track:

| Metric | Meaning |
|---|---|
| provenance coverage | active edges backed by evidence |
| entity merge precision | correct identity resolutions |
| orphan rate | entities without useful links |
| contradiction rate | conflicting active claims |
| stale edge rate | edges outside freshness policy |
| degree distribution | detects hubs/anomalies |
| traversal size | operational/query complexity |
| path validity | supported multi-hop paths |
| tenant isolation failures | security defects |

## 12. Failure-first engineering

Break the system deliberately:

- reverse an edge direction;
- remove provenance;
- create duplicate entities;
- inject a cross-tenant edge;
- allow traversal depth 99;
- add a poisoned relation;
- use stale evidence;
- truncate candidates before authorization filtering.

For each failure record **symptom → evidence → hypothesis → experiment → root cause → fix → regression test**.

## 13. Security model

Treat source content and generated graph proposals as untrusted. Authorization must be evaluated outside the graph. A graph edge can support a decision but cannot grant permission.

Minimum controls: tenant binding, ACL filtering before retrieval, provenance-required edges, bounded traversal, audit events, immutable source identity and independent verification for high-impact actions.

## 14. Production architecture

```text
                 INGESTION
                    |
          +---------+----------+
          |                    |
       evidence             metadata
          |                    |
          +---------+----------+
                    v
             KG BUILD PIPELINE
        extract -> resolve -> validate
                    |
                    v
             versioned graph
              /           \
             v             v
       graph index      vector index
             \             /
              +-----+-----+
                    v
              query planner
                    |
          auth + tenant + budget
                    |
            bounded retrieval
                    |
              rerank/verify
                    |
                 answer
```

## 15. Handoff to Module 32

Module 31 establishes **why explicit knowledge helps** and how to retrieve it. Module 32 makes the graph durable: schema evolution, temporal validity, contradiction management, identity lifecycle, graph migrations and health engineering.
