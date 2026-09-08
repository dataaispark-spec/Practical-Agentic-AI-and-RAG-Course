# Module 35 — Karpathy-style Compounding Knowledge / LLM Wiki

Build a maintained knowledge workspace in which new evidence updates existing knowledge instead of creating an ever-growing pile of disconnected documents.

> This is **Karpathy-inspired compounding knowledge**, not a claim of an official Karpathy methodology.

## Lifecycle

`raw sources → extract → link → validate → compile knowledge pages → detect contradictions → commit → health check → update`

## Labs
1. Create raw/source records.
2. Compile entity and topic pages.
3. Link claims to citations.
4. Resolve duplicate concepts.
5. Record contradictions.
6. Supersede stale knowledge.
7. Generate bounded wiki context for an agent.
8. Measure provenance coverage and knowledge freshness.
9. Inject poisoned knowledge and detect it.
10. Roll back a bad update.

## Required comparison
Benchmark raw document RAG vs curated wiki vs KG vs KG+vector hybrid for the same questions.

## Failure-first
Append-only knowledge, citation loss, stale claims, duplicate concepts, poisoning, context bloat and false authority.

## Production principle
Knowledge should compound through validated evidence, not through unchecked autonomous writing.
