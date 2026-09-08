# Canonical 43-Module Course Map

The course is organized as a 43-module progression. Modules 1–30 retain the IITM-aligned foundation and enterprise Agentic RAG capstone. Modules 31–35 form a dedicated Knowledge Engineering and GraphRAG track; Modules 36–43 build increasingly autonomous agent runtimes and culminate in the frontier Graph-RAG capstone.

## Canonical sequence

30. Enterprise Agentic RAG Capstone
31. Knowledge Engineering & Graph RAG
32. Graph Engineering & Temporal Knowledge
33. Agentic Knowledge Graph Construction
34. Graph + Vector Hybrid Retrieval
35. Karpathy-style Compounding Knowledge / LLM Wiki
36. Loop Engineering
37. Harness Engineering
38. Long-Running Autonomous Agents
39. Skills, Memory & Continual Harnesses
40. Environments, Verifiers & Agentic RL
41. Recursive Self-Improving Agents
42. Computer Use & Always-On Teammates
43. Frontier Graph-RAG Agentic Capstone

## Physical canonical layout

On the `course-43-modules-complete` branch, every canonical module has its own numbered directory. Modules 36–43 are physical mirrors of the mature former 31–38 implementations, preserving the engineering assets while making the GitHub tree match the curriculum numbering.

| Canonical | Subject | Physical directory |
|---:|---|---|
| 31 | Knowledge Engineering & Graph RAG | `31-knowledge-engineering-graph-rag/` |
| 32 | Graph Engineering & Temporal Knowledge | `32-graph-engineering-temporal-knowledge/` |
| 33 | Agentic Knowledge Graph Construction | `33-agentic-knowledge-graph-construction/` |
| 34 | Graph + Vector Hybrid Retrieval | `34-graph-vector-hybrid-retrieval/` |
| 35 | Karpathy-style Compounding Knowledge / LLM Wiki | `35-compounding-knowledge-llm-wiki/` |
| 36 | Loop Engineering | `36-loop-engineering/` |
| 37 | Harness Engineering | `37-harness-engineering/` |
| 38 | Long-Running Autonomous Agents | `38-long-running-autonomous-agents/` |
| 39 | Skills, Memory & Continual Harnesses | `39-skills-memory-continual-harnesses/` |
| 40 | Environments, Verifiers & Agentic RL | `40-environments-verifiers-agentic-rl/` |
| 41 | Recursive Self-Improving Agents | `41-recursive-self-improving-agents/` |
| 42 | Computer Use & Always-On Teammates | `42-computer-use-always-on-ai-teammates/` |
| 43 | Frontier Graph-RAG Agentic Capstone | `43-frontier-graph-rag-agentic-capstone/` |

## Graph engineering definition of done

Modules 31–35 collectively teach ontology/schema design; entities, relations and claims; entity resolution; provenance and citations; temporal validity and supersession; bounded traversal; graph/vector/reranker hybrid retrieval; agentic graph construction and validation; contradiction and poisoning detection; tenant/ACL isolation; graph health metrics; maintained wiki artifacts; and benchmark evidence for when graph structure helps and when it does not.

## Architectural principle

`Knowledge Graph = what the system knows.`

`Agent/Task Graph = how the system works.`

The final AegisAI architecture uses both without allowing either graph to become an unchecked authority. Policy, authorization, budgets, verification, evaluation and audit remain mandatory control boundaries.
