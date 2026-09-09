# 43-Module Completion Manifest

**Status:** normative completion contract  
**Refresh checkpoint:** 2026-09-09  
**Canonical branch:** `main`

This manifest defines the evidence required to call the canonical 43-module course complete. The canonical numbered directories on `main` are authoritative. Historical compatibility copies are not additional modules.

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

### Knowledge engineering & graph — Modules 31–35
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

The source-of-truth paths are:

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

Historical paths, including former `31-loop-engineering` through `38-frontier-agentic-rag-capstone` directories and legacy Module 06/30 aliases, must not receive new canonical links or learning content.

## Module completion contract

Every canonical module must provide evidence for:

```text
Learning objectives
→ README theory / mechanism
→ architecture + data/control flow
→ runnable implementation / lab
→ executable Colab practice
→ guided + independent exercises
→ intentional failure / debugging
→ measurable evaluation
→ security / misuse handling where applicable
→ tests / assertions
→ production trade-offs
→ interview + system-design preparation
→ mastery gate
→ AegisAI + next-module bridge
```

A module is not complete merely because the files exist. Reviewers must be able to locate learner-visible evidence for the material above.

## Notebook completion contract

Canonical notebooks follow:

`Predict → Build → Try → Observe → Break → Debug → Measure → Improve → Defend`

The exact notebook requirements are maintained in [`COLAB-PRACTICE-NOTEBOOK-STANDARD.md`](./COLAB-PRACTICE-NOTEBOOK-STANDARD.md).

## Security completion contract

Relevant modules must cover the appropriate boundaries among identity, tenant, data, memory, tools/MCP, policy, approval, budget, state, verification and audit. Untrusted model/data output must not become authority merely because it is persuasive.

## Evaluation completion contract

Where applicable, learners must measure multiple dimensions such as correctness/quality, retrieval/grounding, safety, reliability, latency and cost. They must interpret trade-offs and preserve meaningful regression evidence.

## Certification contract

Course certification requires all of the following to pass on the current revision:

1. structural 43-module QA;
2. required module-test jobs;
3. clean-kernel notebook-runtime checks;
4. aggregate CI gate;
5. manual semantic review of material content changes and identity drift.

A queued, running, partial, stale or merely expected workflow is not a pass.

## Quality gate

The course should be called **complete** only when it functions as a coherent progressive apprenticeship. Adding files, increasing word counts or making CI less strict does not constitute completion.

See [`COURSE-ENGINEERING-STANDARDS.md`](./COURSE-ENGINEERING-STANDARDS.md) for the authoritative best-practices rules.
