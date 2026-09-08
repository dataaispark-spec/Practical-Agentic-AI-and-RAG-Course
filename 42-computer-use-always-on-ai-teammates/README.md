# Module 42 — Computer Use & Always-On AI Teammates

## Mission
Build an enterprise digital worker that can operate across browser/application environments, maintain durable work state, request approval at trust boundaries, and continue delegated work without requiring a human to drive every step.

## Learning outcomes

By completing this module you can:

1. Distinguish API agents from computer-use agents.
2. Model browser/desktop interaction as a partially observable environment.
3. Build an observation → action → verification loop for UI tasks.
4. Use screenshots, DOM/accessibility information and application state appropriately.
5. Design persistent identity and authorization for digital workers.
6. Implement approval gates for high-impact actions.
7. Handle stale screens, changed UI state, navigation failures and timeouts.
8. Combine deterministic APIs with UI automation where appropriate.
9. Design schedules, event triggers, interruption and resumability.
10. Audit computer actions and capture evidence.
11. Prevent excessive authority and unsafe autonomous continuation.
12. Defend an enterprise always-on worker architecture.

## Hands-on lab — Enterprise Digital Worker

Build a synthetic browser worker with observation, screen/DOM grounding, explicit action schemas, policy checks, approval binding, verification, evidence capture, scheduling and durable state.

### Failure-first cases

Stale screen, hostile page, wrong click, duplicate submission, navigation failure, changed application state, secret exposure and unauthorized action.

### Metrics

Action accuracy, unsafe-action block rate, verification pass rate, recovery rate, audit completeness, cost/hour and task completion.

## Security

Visual confidence is never authorization. Recheck identity, tenant, policy and action scope at the execution boundary; require approval for consequential actions.

## Mastery gate

Demonstrate a safe browser task, survive a stale-state failure, block an unsafe action, produce an audit trail, and explain when deterministic APIs are preferable to UI automation.
