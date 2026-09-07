# ADR-001: Select the Minimum Sufficient AI Architecture

- **Status:** Accepted
- **Date:** 2026-09-07
- **Scope:** Module 1 reference architecture

## Context

AI systems become difficult to operate when architecture grows faster than business value. A request may involve generation, private/current knowledge, actions, or multiple responsibilities, but those requirements should determine the architecture.

## Decision

Use the minimum architecture that satisfies the measured requirements:

1. Deterministic software when generation is unnecessary.
2. An LLM application when generation is required without external knowledge or actions.
3. RAG when private/current knowledge must be supplied at runtime.
4. An agent or explicit workflow when controlled tool/action execution is required.
5. Multi-agent orchestration only after a simpler baseline is benchmarked and evidence shows a meaningful benefit.

## Alternatives considered

### Framework-first development
Rejected because selecting a framework before requirements hides architectural trade-offs.

### Always use RAG
Rejected because some tasks do not need external knowledge.

### Always use an agent
Rejected because unnecessary loops add latency, cost, and failure modes.

### Always use multi-agent
Rejected because coordination complexity needs measurable justification.

## Risks

- Requirements may be incomplete.
- A model may still produce incorrect output.
- Retrieval may return stale or unauthorized information.
- Tools may fail or be invoked with unsafe arguments.

## Controls

- explicit input/output contracts
- identity and authorization before sensitive data access
- tool allowlists and parameter validation
- timeouts and bounded retries
- human approval for high-risk actions
- evaluation datasets and regression tests
- traces, metrics, and incident diagnostics

## Consequences

The system stays easier to reason about and provides a clear baseline for later optimization. The trade-off is that the team must gather requirements and measurement evidence before adding sophisticated orchestration.

## Revisit triggers

Reconsider the decision when measured evidence shows one of the following:

- task success is below requirement
- knowledge freshness cannot be satisfied
- action complexity exceeds the current workflow abstraction
- a multi-agent design demonstrates material task-quality or reliability improvements after accounting for cost and latency
