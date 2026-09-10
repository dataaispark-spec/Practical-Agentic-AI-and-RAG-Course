# Module 33 — Exercises, Labs & Mastery Challenges

## L1–L2 Foundations

1. Explain why model confidence is not truth.
2. Separate proposal, validation, approval and commit.
3. Design a proposal schema with provenance.
4. List five graph-write security threats.

## L3 Build

5. Build a deterministic extractor for entities and relations.
6. Implement canonical proposal hashing.
7. Resolve aliases to stable entity IDs.
8. Validate predicates against a schema allow-list.
9. Implement provenance-required commit.
10. Add idempotent writes.

## L4 Debug

11. Inject an unknown entity.
12. Inject a fabricated citation.
13. Inject a cross-tenant proposal.
14. Inject a contradictory relation.
15. Replay the same proposal after a simulated timeout.
16. Put prompt-injection text inside a source document and prove it cannot redefine policy.

## L5 Optimize

17. Compare rule, NER and LLM extraction on the same labels.
18. Add authority-aware confidence scoring.
19. Tune the human-review threshold using precision and review load.
20. Batch proposals without weakening per-proposal validation.

## L6 Production

21. Design an agentic constructor for 1M updates/day.
22. Design approval queues for high-risk knowledge.
23. Define rollback and audit semantics.
24. Create promotion-quality SLOs and alerts.

## L7 Unfamiliar problem

25. An extraction model becomes more accurate overall but introduces a rare catastrophic false merge. Design a release gate that catches the regression.

## Domain challenge cards

### Cybersecurity
Extract vulnerability relationships from advisories and reject unsupported version claims.

### Banking
Promote fraud-policy relationships only after evidence and risk approval.

### Healthcare
Quarantine unsupported clinical relationships and retain citation spans.

### Manufacturing
Resolve equipment aliases and reject contradictory maintenance relationships.

### Enterprise IT
Construct service dependencies from incident tickets while treating ticket text as untrusted data.

## Failure contract

For each injected fault record: observable, evidence, containment, recovery, regression assertion and residual risk.

## Mastery submission

Submit proposal schema, extraction benchmark, validation pipeline, security tests, approval evidence, idempotency test, rollback evidence and downstream quality comparison.
