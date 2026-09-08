# Repository Refresh — 2026-09-08

## Verified target

Repository: `dataaispark-spec/Practical-Agentic-AI-and-RAG-Course`
Branch: `main`

## What is now present on `main`

- Canonical 43-module curriculum.
- Modules 31–35: Knowledge Engineering + GraphRAG.
- Frontier Modules 36–43 mapped to the mature former 31–38 implementation directories.
- Graph engineering track with knowledge graph + agent/task graph distinction.
- GraphRAG lifecycle: extraction → resolution → provenance/temporal validity → validation → graph/vector/hybrid retrieval → verification → controlled write-back.
- Graph security: poisoning, provenance integrity, tenant/ACL isolation and inference/action boundaries.
- Clean-kernel notebook QA and module-test QA.
- Module 39 notebook fix for the `SkillRegistry` API (`name, version`) mismatch.

## Important numbering clarification

The canonical curriculum is 43 modules, but Modules 36–43 are currently **compatibility-mapped** to the former implementation directories 31–38. This was intentional to preserve mature work while references are migrated. Therefore a user browsing the repository may still see directories such as `31-loop-engineering` even though the canonical subject is Module 36.

Canonical mapping:

| Canonical | Subject | Current implementation |
|---:|---|---|
| 36 | Loop Engineering | `31-loop-engineering/` |
| 37 | Harness Engineering | `32-harness-engineering/` |
| 38 | Long-Running Autonomous Agents | `33-long-running-autonomous-agents/` |
| 39 | Skills, Memory & Continual Harnesses | `34-skills-memory-continual-harnesses/` |
| 40 | Environments, Verifiers & Agentic RL | `35-environments-verifiers-agentic-rl/` |
| 41 | Recursive Self-Improving Agents | `36-recursive-self-improving-agents/` |
| 42 | Computer Use & Always-On Teammates | `37-computer-use-always-on-ai-teammates/` |
| 43 | Frontier Graph-RAG Agentic Capstone | `38-frontier-agentic-rag-capstone/` |

## CI status

The latest Course QA workflow is triggered by the refresh commits. It must finish successfully before the repository is described as QA-certified. A queued workflow is not a passing workflow.

## Next migration rule

Do not delete or blindly rename the mature 31–38 implementation assets. First update all internal references, notebook paths, CI mappings and documentation; then perform a controlled physical directory migration to canonical 36–43 paths.
