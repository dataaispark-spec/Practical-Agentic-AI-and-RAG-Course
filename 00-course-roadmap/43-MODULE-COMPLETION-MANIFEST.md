# 43-Module Completion Manifest

Refresh checkpoint: **2026-09-09**
Branch: **main**

This file is the visible contract for the canonical 43-module course. It records the authoritative curriculum numbering, the current implementation mapping, and the QA certification rule.

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

## Current implementation mapping

Modules 01–30 use their numbered course directories, with `06-rag-from-first-principles/` authoritative over the deprecated `06-rag-first-principles/` duplicate.

Modules 31–35 are physically present at:

- `31-knowledge-engineering-graph-rag/`
- `32-graph-engineering-temporal-knowledge/`
- `33-agentic-knowledge-graph-construction/`
- `34-graph-vector-hybrid-retrieval/`
- `35-compounding-knowledge-llm-wiki/`

Modules 36–43 currently resolve through explicit compatibility mappings to the mature former frontier implementation directories:

- 36 → `31-loop-engineering/`
- 37 → `32-harness-engineering/`
- 38 → `33-long-running-autonomous-agents/`
- 39 → `34-skills-memory-continual-harnesses/`
- 40 → `35-environments-verifiers-agentic-rl/`
- 41 → `36-recursive-self-improving-agents/`
- 42 → `37-computer-use-always-on-ai-teammates/`
- 43 → `38-frontier-agentic-rag-capstone/`

This is intentional and non-destructive: existing tested frontier work is preserved while the canonical numbering is validated centrally by the roadmap and CI. Physical migration of 36–43 can be performed later as a separate rename/copy operation after all references are audited.

## Completion contract

Every canonical module must provide, directly or through its compatibility mapping, the appropriate engineering evidence:

`Learning objectives → README theory → app/lab → executable notebook → exercises → tests → failure/debugging → metrics/evaluation → security → mastery gate`

## QA certification contract

The repository is **not QA-certified** until the current GitHub Actions workflow passes:

1. structural 43-module QA;
2. all module tests in the 04–43 matrix;
3. all clean-kernel notebook-runtime jobs in the 04–43 matrix;
4. final aggregate gate.

A queued or running workflow is not considered a pass.

## Refresh action

The `main` branch was refreshed on **2026-09-09**. The refresh updates the visible canonical contract and intentionally triggers a new Course QA workflow so the GitHub repository, not just local planning notes, becomes the source of truth for the current state.
