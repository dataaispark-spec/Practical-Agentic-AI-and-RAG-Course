# 43-Module Completion Branch

This branch is the canonical physical layout of the 43-module Agentic AI & RAG Engineering course.

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

## Physical repository contract

Every module is expected to expose its teaching material plus executable engineering assets. The mature frontier implementations from the previous numbering are physically mirrored into their canonical 36–43 directories on this branch so the GitHub tree visibly matches the 43-module curriculum.

## Quality contract

- Ready-to-execute notebooks are part of the course deliverable.
- Labs/exercises and tests are part of the engineering learning loop.
- Failure-first debugging is required.
- Module tests and clean-kernel notebook runtime checks are required before QA certification.
- CI must be treated as a gate, not as documentation.

## Migration note

The old frontier directories are intentionally retained in this branch for compatibility while canonical paths are validated. They can be removed in a later cleanup commit only after all references and CI paths are proven canonical.
