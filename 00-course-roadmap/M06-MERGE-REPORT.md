# Module 06 consolidation report

## Decision
`06-rag-from-first-principles/` is the canonical Module 6 implementation.

## Evidence
- It contains the richer first-principles application split (`models`, `chunker`, `embeddings`, `index`, `retriever`, pipeline-facing components) and the corresponding tests.
- Its README defines the intended build order, retrieval/generation separation, evaluation metrics, failure lab, production architecture, interview bank, mastery gate, and gold challenge.
- `06-rag-first-principles/` is a duplicate/older scaffold with a second `rag.py` implementation and a smaller notebook surface.
- The CI workflow has already been normalized to execute the canonical `06-rag-from-first-principles` directory for Module 06.

## Cleanup policy
The duplicate directory must not be treated as a second course module. Its historical README remains as a redirect/deprecation marker until all references are verified and the redundant implementation/notebook/tests are removed.

## Compatibility rule
Do not silently merge APIs with incompatible contracts. The canonical implementation wins; useful concepts from the older implementation are retained through the canonical module's documented metadata, authorization, evidence, and abstention requirements.

## QA requirement
After cleanup, the Module 06 test job and notebook-runtime job must both pass. The final course QA gate must count Module 06 exactly once.
