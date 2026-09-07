# Module 15 — Agent Memory Engineering

## Mission
Build memory as an engineered subsystem—not as “put everything into the prompt.” The goal is to decide what should be remembered, how it is retrieved, when it expires, how it is corrected, and how access is controlled.

## Mental model
```text
Experience → Extract → Validate → Store → Retrieve → Rank → Inject → Use → Verify → Consolidate / Forget
```

Agent memory is state that survives beyond the immediate reasoning step. Different memory classes solve different problems.

## Memory taxonomy
| Memory | Purpose | Typical lifetime | Example |
|---|---|---|---|
| Working | Current task state | seconds/minutes | active plan |
| Episodic | Past events | days/years | previous incident |
| Semantic | Stable facts | long-lived | company policy |
| Procedural | How to perform a task | long-lived/versioned | troubleshooting procedure |
| User/task | Preferences and constraints | governed | preferred report format |
| Tool/environment | External state | variable | last deployment |

Do not collapse all of these into one vector database.

## Memory record contract
A production memory record should have at least:
- memory ID;
- tenant/user scope;
- type;
- content;
- source/provenance;
- created/updated time;
- confidence;
- importance;
- sensitivity/classification;
- expiry policy;
- version;
- supersession relationship;
- embedding/model version when applicable.

## Retrieval
A useful memory score can combine:

`score = relevance × confidence × importance × freshness × permission`

The formula is illustrative; the course requires benchmarking alternatives rather than treating one scoring formula as universal.

## Consolidation
Raw episodes should not automatically become permanent facts.

Example:
```text
100 support interactions
       ↓
extract candidate facts
       ↓
validate + deduplicate
       ↓
resolve contradictions
       ↓
store semantic/procedural memory
       ↓
retain source episodes for audit
```

## Contradiction handling
Never silently overwrite conflicting memories. Track:
- competing values;
- evidence and timestamps;
- source authority;
- confidence;
- supersession decision;
- human review where impact is high.

## Forgetting
Memory needs deletion and expiry as first-class operations.

Strategies to implement and compare:
- TTL;
- inactivity decay;
- bounded capacity;
- importance thresholds;
- policy-driven retention;
- user-requested deletion;
- legal/compliance deletion workflows.

## Security
Memory is a high-value persistence layer and a major attack surface.

Protect against:
- memory poisoning;
- prompt injection stored as “facts”;
- cross-tenant leakage;
- unauthorized recall;
- sensitive-data retention;
- stale permissions;
- indirect prompt injection through retrieved memories.

Treat recalled memory as **untrusted context**, not as system instructions.

## Lab 1 — Working memory
Build a bounded task state store. Prove that unrelated history is not injected into every step.

## Lab 2 — Episodic memory
Store agent trajectories as events and retrieve prior episodes using deterministic relevance rules.

## Lab 3 — Semantic memory
Extract candidate facts from episodes, attach provenance and confidence, and require validation before promotion.

## Lab 4 — Procedural memory
Store reusable procedures separately from factual knowledge. Version every procedure.

## Lab 5 — Memory retrieval
Implement keyword retrieval, recency scoring and hybrid scoring. Benchmark precision@K and irrelevant-memory rate.

## Lab 6 — Contradiction lab
Insert two conflicting facts. Implement conflict detection, authority ranking and explicit resolution records.

## Lab 7 — Forgetting lab
Implement TTL, importance decay and manual deletion. Verify expired memories cannot be recalled.

## Lab 8 — Poisoning lab
Inject a malicious memory such as “ignore all security policies.” Prove policy remains authoritative and memory is treated as data.

## Lab 9 — Multi-tenant memory
Create tenant A and tenant B. Prove every read and write is scoped and test adversarial cross-tenant queries.

## Lab 10 — Memory-aware agent
Connect Module 14's raw agent loop to memory. Compare no-memory, episodic-memory and semantic-memory agents on repeated tasks.

## Detailed exercises
1. Define a memory schema.
2. Add provenance.
3. Add confidence and importance.
4. Implement tenant isolation.
5. Implement TTL.
6. Implement deletion.
7. Implement recency decay.
8. Implement relevance ranking.
9. Add contradiction detection.
10. Add supersession links.
11. Add memory promotion rules.
12. Add memory demotion rules.
13. Separate procedural from semantic memory.
14. Add embedding version metadata.
15. Build a memory inspection CLI.
16. Build memory replay tests.
17. Measure irrelevant recall.
18. Measure useful-memory hit rate.
19. Benchmark context-token savings.
20. Build a memory corruption recovery procedure.

## Failure-first exercises
### Memory poisoning
A user-controlled message becomes a persistent “instruction.” Detect and quarantine it.

### Stale memory
A previously correct policy is superseded. Ensure the newer authoritative source wins.

### Contradiction
Two sources disagree. Do not silently merge them.

### Permission drift
A user loses access after memory was stored. Retrieval must enforce current authorization.

### Cross-tenant leakage
Search intentionally uses a broad query. Verify tenant filtering occurs before final context injection.

### Memory explosion
Store thousands of low-value memories. Prove bounded retrieval and consolidation prevent context growth.

### False confidence
A memory has weak provenance but high similarity. Ensure relevance alone cannot make it authoritative.

## Metrics
Track:
- useful-memory hit rate;
- irrelevant-memory rate;
- memory precision@K;
- stale-memory rate;
- contradiction rate;
- promotion accuracy;
- deletion correctness;
- cross-tenant violation count;
- context-token savings;
- memory storage cost;
- retrieval latency.

## Production architecture
```text
                 ┌───────────────┐
Agent Loop ─────▶│ Memory Gateway│
                 └──────┬────────┘
                        │
       ┌────────────────┼─────────────────┐
       ▼                ▼                 ▼
 Working Store    Episodic Store    Semantic/Procedural
       │                │                 │
       └────────────────┼─────────────────┘
                        ▼
                Retrieval + Ranking
                        ▼
                Policy / ACL Filter
                        ▼
                  Context Builder
                        ▼
                     Agent
```

## Industry scenarios
**Banking:** customer preference memory must respect current consent, authorization and retention policies.

**Healthcare:** clinical memory requires provenance, temporal validity and strict access control.

**Cybersecurity:** incident memories should preserve evidence lineage while preventing malicious historical instructions from becoming executable policy.

**Enterprise IT:** procedural memories can improve repeated troubleshooting while remaining versioned against changing runbooks.

## Interview questions
1. Why isn't a vector database sufficient for agent memory?
2. Difference between episodic, semantic and procedural memory?
3. What should never be persisted automatically?
4. How do you handle contradictory memories?
5. How do you prevent memory poisoning?
6. How do you enforce deletion?
7. How do permissions interact with old memories?
8. Why retain provenance?
9. How do you evaluate memory retrieval?
10. How would you migrate embedding versions?
11. How do you prevent memory from increasing prompt size indefinitely?
12. How would you design tenant isolation?
13. What belongs in working memory vs durable memory?
14. When should a memory be promoted?
15. How would you debug a wrong agent decision caused by memory?

## System-design challenge
Design a multi-tenant memory service for 100,000 agents with durable state, semantic retrieval, ACL enforcement, deletion, contradiction tracking, auditability and p95 retrieval under a strict latency budget.

## Mastery gate
Build a memory-aware agent that can learn a validated fact from one task, retrieve it on a later task, reject poisoned memory, handle contradictory evidence and honor deletion/authorization requirements.

## Gold challenge
Run the same benchmark with no memory, episodic memory, semantic memory and hybrid memory. Measure task success, irrelevant recall, latency, context tokens, cost, stale-memory errors and security violations. Defend the memory architecture using evidence.

## Google Colab
`notebooks/module_15_memory.ipynb` contains a self-contained implementation with working, episodic and semantic memory, retrieval scoring, contradiction detection, TTL/deletion, tenant isolation, poisoning tests and extension exercises.
