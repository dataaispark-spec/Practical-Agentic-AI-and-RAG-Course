# Runtime QA Status — 2026-09-08

## Checkpoint purpose

This checkpoint records the latest repository state after the Module 06 consolidation, Module 06–09 hardening pass, and CI workflow correction. It deliberately separates **implemented changes** from **verified runtime evidence**.

## Implemented at this checkpoint

- Course-wide `requirements-dev.txt` for pytest and notebook execution.
- `00-course-roadmap/run_notebook_qa.py` for clean-kernel notebook execution with mock-provider defaults.
- CI with structural QA, a 35-way module-test matrix, a 35-way notebook-runtime matrix, and a final aggregate gate.
- CI module identifiers are now explicit zero-padded strings (`04` … `38`), preventing YAML numeric coercion from breaking directory resolution.
- Module test jobs isolate each module's local `app/` package through `PYTHONPATH`.
- Production-shaped runtime implementations/tests for Modules 31–37:
  - M31 loop engine
  - M32 harness boundary
  - M33 durable worker
  - M34 gated skill registry
  - M35 environment/verifier kernel
  - M36 bounded self-improvement experiment engine
  - M37 governed computer-use sandbox
- Module 06 has been consolidated to the canonical `06-rag-from-first-principles/` implementation; obsolete duplicate code/tests/notebook artifacts under `06-rag-first-principles/` were removed.
- M06 hardening: deterministic tie-breaking and filter-before-ranking/truncation behavior.
- M07 hardening: deterministic cross-process embeddings, dimension validation, tenant-safe filtering, deterministic ranking, and explicit Recall@K semantics.
- M08 hardening: document lineage/provenance, deterministic PII handling/redaction, quarantine behavior, ACL validation, and source/protected hashes.
- M09 hardening: deterministic lexical+dense retrieval, RRF/reranking, metadata filtering, and authorization before candidate truncation.
- Root `README.md` refreshed to reflect the 38-module checkpoint and the evidence-based definition of done.

## Evidence already established

The repository inspection confirms the above files/changes are present on `main`. The latest CI run before the workflow correction was still queued and therefore was not valid evidence of final success. Earlier runtime evidence had exposed module-path/import problems, including the zero-padding issue in the CI matrix; the workflow has now been corrected rather than assuming those jobs passed.

## Current CI state

A new push-triggered QA run is expected from the workflow correction and README/status updates. **Do not interpret the presence of queued jobs as a pass.** Final status must be taken from the completed structural, module-test, notebook-runtime, and aggregate-gate jobs for the current revision.

## Non-claims

- This checkpoint does **not** declare the 38-module QA gate passed.
- Structural QA is not runtime QA.
- Passing tests is not proof of pedagogical completeness.
- Passing notebooks is not proof that every module contains sufficient depth, failure injection, measurement, solutions, and industry context.
- The educational implementations are not automatically production infrastructure; their module READMEs must state scope and limitations.

## Next verification gate

1. Inspect the new CI run and all matrix jobs.
2. Capture every failing module test and notebook execution failure.
3. Fix failures at source and rerun.
4. Verify Modules 31–38 app/test/notebook integration.
5. Audit notebook depth against `COLAB-PRACTICE-NOTEBOOK-STANDARD.md`.
6. Confirm no duplicate or ambiguous canonical module paths remain.
7. Only after all evidence is green, update this checkpoint and the root README to record **38-module QA complete**.
