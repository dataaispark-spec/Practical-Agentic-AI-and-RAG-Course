# Module 42 — Computer Use & Always-On AI Teammates

**Canonical implementation:** `42-computer-use-always-on-ai-teammates/`. Former `37-computer-use-always-on-ai-teammates/` is legacy only.

## Mission
Build enterprise digital workers that can operate across browsers/applications, maintain durable work state, request approval at trust boundaries and continue delegated work without uncontrolled authority.

## Learning outcomes
Distinguish API agents from computer-use agents; model UI environments; combine screenshot/DOM/accessibility observations; validate actions; detect stale state; implement approvals, persistent identity, schedules, recovery, DLP and audit.

## Architecture
```text
Goal → Agent Loop → Observation + Policy → Action Planner
                         ↓                    ↓
                  Screenshot/DOM/A11y   Mouse/Keyboard/API
                         ↓                    ↓
                         Environment → Verification
```

Prefer `API → native integration → computer use` when structured interfaces exist.

## Labs
1. Screenshot vs DOM vs accessibility observations.
2. Typed UI action contract.
3. Precondition/postcondition verification.
4. Stale-state detection.
5. High-impact approval gates.
6. Persistent identity and least privilege.
7. Event/schedule-triggered workers.
8. API-first/UI-second benchmark.
9. Prompt injection embedded in webpage content.
10. DLP/credential-exfiltration prevention.
11. Crash after external submission and reconciliation.
12. Session expiry recovery.
13. Always-on runaway trigger loop.
14. AegisAI digital worker.

## Exercises
Design a customer-operations worker, defend identity/credential isolation, approval expiry, browser sandboxing, verification and emergency shutdown. Measure UI actions versus API actions per successful task.

## Measures
Task success, action success, stale-action rate, verification failure, unsafe-action attempts, approval rate, recovery rate, cost/task and trigger-loop rate.

## Security
Treat webpage/application text as untrusted input. High-impact actions require policy and, where appropriate, human approval. Credentials are isolated and data transfers pass deterministic DLP controls.

## Mastery gate
Demonstrate a sandboxed worker that survives stale UI state, ignores page injection, invalidates stale approval, verifies consequential actions, persists state and emits complete audit evidence.
