# Runtime QA Status — 2026-09-08

## Scope
Modules 04–38, with special attention to notebook execution, module test isolation, dependency reproducibility, frontier implementation depth, and the Module 06 duplicate.

## Implemented in this pass

- Course-wide `requirements-dev.txt` for pytest + notebook execution.
- `00-course-roadmap/run_notebook_qa.py` for clean-kernel notebook execution with mock-provider defaults.
- CI now has structural QA, a 35-way module-test matrix, a 35-way notebook-runtime matrix, and a final aggregate gate.
- CI module test jobs isolate each module's local `app/` package through `PYTHONPATH`.
- Added production-shaped runtime implementations and tests for Modules 31–37 where frontier material was previously notebook/README heavy:
  - M31 loop engine
  - M32 harness boundary
  - M33 durable worker
  - M34 gated skill registry
  - M35 environment/verifier kernel
  - M36 bounded self-improvement experiment engine
  - M37 governed computer-use sandbox

## First runtime findings

The first execution pass immediately found a real packaging/import defect in existing modules 12 and 19: their tests import `app.*`, but the original CI job only exposed repository root on `PYTHONPATH`. This is now corrected in the workflow by adding each module directory and its `app/` directory to the test path.

The first structural QA job passed. Notebook jobs and remaining module-test jobs are intentionally still treated as runtime evidence rather than assumed green.

## Important non-claims

- This file does not declare the 38-module final QA gate passed.
- A successful notebook execution does not by itself prove pedagogical completeness.
- A structural QA pass does not prove runtime correctness.
- The Module 06 duplicate has not been deleted automatically; content must be compared and merged deliberately.

## Next gate

1. Complete current CI matrix.
2. Capture every failing module/notebook.
3. Fix failures and rerun.
4. Add missing module-specific reference implementations rather than generic scaffolds.
5. Consolidate Module 06.
6. Verify frontier modules 31–38 against the deep-practice notebook standard.
7. Run final 38-module structural + test + notebook gate.
