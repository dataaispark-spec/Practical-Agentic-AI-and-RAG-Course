# Practical Agentic AI and RAG Course

> Industry-oriented companion course and hands-on engineering lab built around the IITM Pravartak Agentic AI & RAG curriculum and extended into knowledge engineering, GraphRAG and frontier agent engineering.

This repository follows a **43-module canonical learning journey**. Modules 1–30 preserve the core progression. Modules 31–35 add a dedicated knowledge-engineering track; Modules 36–42 build progressively autonomous agent runtimes; Module 43 integrates the complete system.

## Canonical 43-module progression

### Foundation — Modules 1–5
1. AI Systems Thinking & Architecture Decisions
2. Python for AI Engineering
3. FastAPI + Testing
4. LLM Application Foundations
5. Prompting + Evaluation

### RAG Engineering — Modules 6–12
6. RAG From First Principles
7. Embeddings + Vector Databases
8. Document Intelligence + PII
9. Advanced Retrieval
10. RAG Optimization
11. RAG Evaluation
12. RAG Debugging

### Agent Engineering — Modules 13–18
13. Tool Calling + API Agents
14. Raw Agent Loop
15. Memory
16. LangGraph / Stateful Workflows
17. Planning + Human-in-the-Loop
18. Agent Security

### Multi-Agent Systems — Modules 19–22
19. Single vs Multi-Agent Decision Science
20. Multi-Agent Architectures
21. Coordination + Fault Tolerance
22. Multi-Agent Debugging

### MCP — Modules 23–24
23. MCP Fundamentals
24. Enterprise MCP Server

### Production AI — Modules 25–30
25. Observability
26. Production Evaluation + Regression
27. Cost Engineering
28. Responsible AI + Security
29. Deployment + CI/CD
30. **Enterprise Agentic RAG Capstone**

### Knowledge Engineering + GraphRAG — Modules 31–35
31. **Knowledge Engineering & Graph RAG**
32. **Graph Engineering & Temporal Knowledge**
33. **Agentic Knowledge Graph Construction**
34. **Graph + Vector Hybrid Retrieval**
35. **Karpathy-style Compounding Knowledge / LLM Wiki**

### Frontier Agent Engineering — Modules 36–43
36. Loop Engineering
37. Harness Engineering
38. Long-Running Autonomous Agents
39. Skills, Memory & Continual Harnesses
40. Environments, Verifiers & Agentic RL
41. Recursive Self-Improving Agents
42. Computer Use & Always-On Teammates
43. **Frontier Graph-RAG Agentic Capstone**

## Canonical implementation paths

The canonical 43-module numbering is authoritative. Existing mature frontier implementations are retained under their former paths where necessary; the compatibility map explicitly resolves canonical modules 36–43 to those implementations. This avoids deleting tested material merely to rename directories.

See:

- `00-course-roadmap/CANONICAL-43-MODULE-MAP.md`
- `00-course-roadmap/43-MODULE-COMPLETION-MANIFEST.md`
- `00-course-roadmap/GRAPH-ENGINEERING-TRACK.md`

## Graph engineering

The course deliberately teaches **two different graphs**:

```text
Knowledge Graph              Agent / Task Graph
what the system knows        how the system works
entities                     goals
relations                    states
claims                       transitions
provenance                   tools/workers
validity/time                recovery/approval
```

Modules 31–35 cover ontology/schema design, entities, relations, claims, provenance, temporal validity, entity resolution, contradiction handling, bounded traversal, graph poisoning, tenant/ACL isolation, graph/vector hybrid retrieval, GraphRAG evaluation, graph health and compounding knowledge.

The progression is:

**Know → Retrieve → Construct → Connect → Compound → Reason → Operate → Persist → Learn → Improve → Act.**

## Frontier control plane

Every autonomous capability must explicitly account for:

```text
Goal → Loop → State → Tools → Policy → Budget
 → Verification → Recovery → Evaluation
 → Improvement → Security → Audit
```

Mental model:

```text
Agent = Model + Harness + Environment + Tools + State
      + Policy + Verification + Evaluation + Improvement
```

## Failure-first engineering

Labs intentionally inject retrieval failures, stale/poisoned knowledge, malformed tools, prompt injection, memory poisoning, tenant leakage, infinite loops, retry storms, worker crashes, stale checkpoints, duplicate side effects, coordination failures, cost explosions, reward hacking, benchmark leakage, UI drift and unsafe autonomous actions.

Every meaningful failure should produce an observable incident, root cause, containment/recovery path and regression test.

## Colab / hands-on contract

Every canonical module is expected to provide executable practice following:

**Predict → Run → Observe → Explain → Break → Debug → Measure → Improve → Defend**

The repository's notebook runner executes notebooks in a clean kernel and module-local Python path. Notebook existence alone is not treated as proof of runtime correctness.

## QA and restart status

The repository contains a 43-module structural gate, module-test matrix, notebook-runtime matrix and final aggregate gate:

- `00-course-roadmap/course_qa_checker.py --strict`
- `00-course-roadmap/run_notebook_qa.py`
- `.github/workflows/course-qa.yml`

**Refresh checkpoint: 2026-09-09.** This commit intentionally refreshes the canonical course contract on `main` and triggers a fresh GitHub Actions validation run. The course must not be described as QA-certified until the complete current matrix passes.

## Continuous capstone — AegisAI

AegisAI evolves from a simple AI application into a governed enterprise Agentic RAG and autonomous-work platform containing retrieval, knowledge graph, hybrid GraphRAG, memory, skills, MCP, tools, harness, durable workers, verification, evaluation, governance and computer use.

## Engineering principles

1. Framework second, mechanism first.
2. Deterministic control around probabilistic decisions.
3. Verification is first-class.
4. Persistence changes the threat model.
5. Self-improvement requires external gates.
6. More agents are not automatically better.
7. Graphs are evidence, not unchecked authority.
8. Temporal and provenance semantics matter for enterprise knowledge.
9. Computer use requires environment grounding, approval and post-action verification.
10. Production quality is demonstrated by tests, measurements and failure recovery—not by demos alone.
