# 43-Module Content Alignment Audit — refreshed 2026-09-09

**Repository:** `dataaispark-spec/Practical-Agentic-AI-and-RAG-Course`  
**Canonical branch:** `main`

This is an engineering audit, not a claim that file counts alone prove pedagogical quality. The audit checks module identity, theory/README alignment, implementation/lab boundaries, Colab notebooks, exercises, tests, measurements, security and capstone progression.

## Audit contract

For every module:

`Objective → theory/README → architecture → implementation/lab → Colab → exercise → test → measurement → mastery gate`

A module is not considered release-ready merely because its notebook executes.

## Canonical sequence

01–05 foundations; 06–12 RAG; 13–18 tools/loops/memory/state/planning/security; 19–24 multi-agent/MCP; 25–30 productionization and first capstone; 31–35 knowledge/graph engineering; 36–43 frontier loops, harnesses, durability, continual skills, environments/verifiers, self-improvement, computer use and final capstone.

## Current structural findings

The repository contains canonical numbered directories through Module 43. Historical former 31–38 directories remain as compatibility copies and must not be treated as authoritative implementations. Module 06 is canonical at `06-rag-from-first-principles`; Module 30 is canonical at `30-enterprise-agentic-rag-capstone`.

Several frontier canonical directories originally contained thin README wrappers and notebooks retaining historical module numbers. This is a real documentation/identity defect, even when the underlying implementation is technically relevant. Canonical README titles and notebook metadata must use the canonical module number.

## Runtime defects found by Course QA run #123

The live GitHub Actions run on the pre-fix head exposed three concrete test defects:

1. **M08** — card-like payment data overlapped the broad phone detector, so a low-confidence card value was redacted as phone data and was not quarantined. The detector now gives card-like spans precedence over the broad phone pattern.
2. **M22** — `assert d:=TraceDebugger(es)` is invalid Python syntax. The test now constructs `d` explicitly and asserts against it.
3. **M27** — exact equality on binary floating-point cost (`0.30000000000000004 == 0.3`) made the test flaky/incorrect. The test now uses `pytest.approx`.

The structural checker also identified genuine repository gaps: M02 and M10 lacked an application boundary, and M06 lacked a canonical executable notebook. Those artifacts have now been added.

## QA checker improvements

`course_qa_checker.py` was strengthened to:

- resolve the canonical path for every module 01–43;
- distinguish the canonical M06/M30 paths from legacy aliases;
- accept semantically equivalent notebook section labels rather than brittle exact marker strings;
- use substantial lexical overlap for objective evidence rather than punctuation-sensitive exact phrases;
- continue to require README identity, notebook presence, app boundary, tests and explicit learning/mastery evidence.

This reduces false negatives without weakening the requirement that every module contain observable build/experiment/failure/measurement evidence.

## Content review dimensions

### README / theory

Check: mission, learning outcomes, mechanism, architecture, production trade-offs, failure modes, security, exercises, interview questions, system design and mastery gate.

### Labs / implementation

Check: executable reference implementation, deterministic fixtures where practical, provider-independent CI path, failure injection and recovery.

### Colab

Required learning loop:

`Predict → Run → Observe → Explain → Break → Debug → Measure → Improve`

External API keys are not required for the baseline QA notebooks.

### Exercises

Exercises must force design/implementation/debugging/optimization/defense rather than passive reading. Gold challenges should connect to AegisAI.

### Architecture

Every module should make trust boundaries, state, data flow, failure handling and deterministic-vs-probabilistic responsibilities explicit.

### Tests

Tests must cover both happy paths and failure invariants. Tests themselves are reviewed for syntax, floating-point correctness, determinism and meaningful assertions.

### Security

Tenant boundaries, authorization, provenance, policy isolation, secret handling, prompt injection, persistence poisoning and consequential-action verification are checked where applicable.

### Progression

No frontier module should duplicate another module's primary learning objective. The graph track precedes the frontier autonomy track; M36 starts the loop/harness frontier after M31–35 knowledge engineering.

## Certification rule

The course is **not certified** until a fresh GitHub Actions run passes:

1. structural alignment QA;
2. module-test matrix M04–M43;
3. canonical notebook-runtime matrix M04–M43;
4. aggregate gate;
5. manual review of any newly introduced identity/content drift.

A green CI run is necessary but not sufficient for pedagogical certification.

## Next audit gate

After every corrective commit, rerun the complete matrix. Do not suppress failures merely to obtain green CI; fix the underlying invariant or explicitly document a justified test-contract change.
