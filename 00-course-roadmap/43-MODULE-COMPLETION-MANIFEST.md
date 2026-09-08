# 43-Module Completion Branch

This branch is the canonical 43-module learning branch. The numbered directories `01`–`43` are the authoritative curriculum paths. Legacy frontier directories from the former 31–38 numbering are retained only as compatibility copies and must not receive new learning content.

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

## Completion contract

Every canonical module must provide learning material and executable engineering evidence appropriate to its subject:

`Learning objectives → README theory → app/lab → executable notebook → exercises → tests → failure/debugging → metrics/evaluation → security → mastery gate`

A notebook's existence is not evidence of pedagogical completeness; the content must demonstrate the module objectives through executable practice where applicable.

## QA contract

The branch is not considered QA-certified until:

1. structural 43-module QA passes;
2. module tests pass;
3. clean-kernel notebook runtime tests pass;
4. objective-to-artifact alignment QA passes;
5. canonical module identity checks pass;
6. the final aggregate CI gate passes.

## Duplicate-path policy

`06-rag-first-principles/` is a deprecated duplicate; `06-rag-from-first-principles/` is authoritative.

Former frontier directories `31-loop-engineering/` through `38-frontier-agentic-rag-capstone/` are compatibility copies only. New work belongs in canonical `36-loop-engineering/` through `43-frontier-graph-rag-agentic-capstone/`.
