# 43-Module Upgrade Status — 2026-09-08

## Canonical curriculum

The course is now canonically organized as Modules 1–30 plus a 13-module frontier extension (31–43).

### New knowledge-engineering sequence

31. Knowledge Engineering & Graph RAG
32. Graph Engineering & Temporal Knowledge
33. Agentic Knowledge Graph Construction
34. Graph + Vector Hybrid Retrieval
35. Karpathy-style Compounding Knowledge / LLM Wiki

### Existing frontier sequence moved in the canonical map

36. Loop Engineering
37. Harness Engineering
38. Long-Running Autonomous Agents
39. Skills, Memory & Continual Harnesses
40. Environments, Verifiers & Agentic RL
41. Recursive Self-Improving Agents
42. Computer Use & Always-On Teammates
43. Frontier Graph-RAG Agentic Capstone

## Implemented in this upgrade

- canonical 43-module map;
- root README updated to the 43-module progression;
- structural QA checker upgraded from 38 to 43 canonical modules;
- notebook QA runner upgraded with canonical compatibility mapping;
- CI matrix upgraded to 43 module-tests and 43 notebook-runtime jobs;
- Modules 31–35 now have dedicated README, executable app primitive, tests, Colab notebook and 15 exercises;
- existing mature Modules 31–38 implementation assets preserved and mapped to canonical Modules 36–43;
- GraphRAG, temporal knowledge, agentic KG construction, hybrid retrieval, provenance, graph security and compounding-knowledge requirements are now explicit.

## Important compatibility decision

Physical directory renaming is deliberately deferred until all external links and internal references can be migrated atomically. The canonical map is the source of truth during this transition. No mature frontier implementation was deleted merely to change numbering.

## QA execution

A push to the updated CI workflow has been triggered. The workflow now requires structural QA plus module tests plus clean-kernel notebook execution for the canonical 43-module matrix.

A green result must be observed on the current revision before declaring QA complete. Earlier failures remain relevant until the new run demonstrates that they are resolved.
