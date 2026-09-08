# 43-Module Completion Manifest

Refresh checkpoint: **2026-09-09**  
Branch: **main**

This is the visible completion contract for the canonical 43-module course. The numbered directories on `main` are authoritative; historical frontier directories are compatibility copies only.

## Canonical sequence

### Core — Modules 01–30
1. AI Systems Thinking & Architecture Decisions
2. Python for AI Engineering
3. FastAPI + Testing
4. LLM Application Foundations
5. Prompting + Evaluation
6. RAG From First Principles
7. Embeddings + Vector DB
8. Document Intelligence + PII
9. Advanced Retrieval
10. RAG Optimization
11. RAG Evaluation
12. RAG Debugging
13. Tool Calling + API Agents
14. Raw Agent Loop
15. Memory
16. LangGraph Stateful Workflows
17. Planning + Human-in-the-Loop
18. Agent Security
19. Multi-Agent Reality Check
20. Multi-Agent Architectures
21. Coordination + Fault Tolerance
22. Multi-Agent Debugging
23. MCP Fundamentals
24. MCP Server — Enterprise
25. Observability
26. Production Evaluation
27. Cost Engineering
28. Responsible AI + Governance
29. Deployment + CI/CD
30. Enterprise Agentic RAG Capstone

### Knowledge Engineering & Graph track — Modules 31–35
31. Knowledge Engineering & Graph RAG
32. Graph Engineering & Temporal Knowledge
33. Agentic Knowledge Graph Construction
34. Graph + Vector Hybrid Retrieval
35. Karpathy-style Compounding Knowledge / LLM Wiki

### Frontier agent engineering — Modules 36–43
36. Loop Engineering
37. Harness Engineering
38. Long-Running Autonomous Agents
39. Skills, Memory & Continual Harnesses
40. Environments, Verifiers & Agentic RL
41. Recursive Self-Improving Agents
42. Computer Use & Always-On AI Teammates
43. Frontier Graph-RAG Agentic Capstone

## Canonical implementation mapping

Modules **01–43 have canonical numbered directories on `main`**:

`01-ai-systems-thinking/` through `30-enterprise-agentic-rag-capstone/`, followed by:

- `31-knowledge-engineering-graph-rag/`
- `32-graph-engineering-temporal-knowledge/`
- `33-agentic-knowledge-graph-construction/`
- `34-graph-vector-hybrid-retrieval/`
- `35-compounding-knowledge-llm-wiki/`
- `36-loop-engineering/`
- `37-harness-engineering/`
- `38-long-running-autonomous-agents/`
- `39-skills-memory-continual-harnesses/`
- `40-environments-verifiers-agentic-rl/`
- `41-recursive-self-improving-agents/`
- `42-computer-use-always-on-ai-teammates/`
- `43-frontier-graph-rag-agentic-capstone/`

The former `31-loop-engineering/` through `38-frontier-agentic-rag-capstone/` paths remain only as legacy compatibility copies and must not be used for new canonical links.

## Completion contract

Each canonical module is expected to expose:

`Learning objectives → README theory → architecture → app/lab → executable Colab → exercises → tests → failure/debugging → metrics/evaluation → security → mastery gate`

The notebook learning contract is:

`Predict → Build → Try → Break → Debug → Measure → Improve → Defend`

Equivalent section names are acceptable when the executable behavior is present.

## QA certification contract

The repository is **not QA-certified** until the current GitHub Actions workflow passes all of:

1. structural 43-module QA;
2. module-test matrix;
3. clean-kernel notebook-runtime matrix;
4. aggregate gate.

A queued, running, or partially successful workflow is **not** a pass.

## Audit principle

Automated QA proves structural/runtime invariants. Major curriculum changes additionally require manual semantic review of theory, architecture, lab realism, exercise progression, failure coverage, measurement, security and capstone integration.
