# Module 33 — Agentic Knowledge Graph Construction

Teach agents to construct and maintain knowledge graphs safely: extract → resolve → propose → validate → approve → commit → monitor → rollback.

## Core topics
Entity/claim/relation extraction, confidence, provenance, entity resolution, contradiction handling, human approval for sensitive knowledge, write-back idempotency, versioning and rollback.

## Labs
1. Build a deterministic extractor.
2. Propose entities and relations.
3. Resolve duplicates.
4. Reject unsupported relations.
5. Require provenance.
6. Detect contradictions.
7. Validate before commit.
8. Simulate graph poisoning.
9. Roll back a bad update.
10. Measure extraction precision and graph health.

## Failure contract
Every injected fault must identify the expected observable, failure class, containment, recovery and regression assertion.

## Security
Treat extracted knowledge as untrusted until validated. A model-generated edge never grants permission to act.
