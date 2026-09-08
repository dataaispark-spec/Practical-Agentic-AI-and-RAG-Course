# AegisAI Capstone — Implementation Build Plan

## Stage 0 — Contracts first

- [x] Task contract
- [x] Action contract
- [x] Risk/action classification
- [x] Policy decision object
- [x] Bounded loop state machine
- [x] Core tests

## Stage 1 — Deterministic execution kernel

- [ ] Durable run store
- [ ] Checkpoint schema
- [ ] Event/audit schema
- [ ] Idempotency store
- [ ] Budget manager
- [ ] Cancellation

## Stage 2 — Tool gateway

- [ ] Tool registry
- [ ] JSON/schema validation
- [ ] Authorization middleware
- [ ] Timeout/retry policy
- [ ] Side-effect classification
- [ ] Tool telemetry

## Stage 3 — RAG

- [ ] Document model
- [ ] Ingestion pipeline
- [ ] Chunking
- [ ] Embedding interface
- [ ] Lexical retrieval
- [ ] Vector retrieval interface
- [ ] Hybrid ranking
- [ ] Evidence objects
- [ ] Retrieval evaluation dataset

## Stage 4 — Agent runtime

- [ ] Model adapter
- [ ] Structured decision output
- [ ] Context builder
- [ ] Agent loop integration
- [ ] Termination policy
- [ ] Recovery policy

## Stage 5 — Memory and skills

- [ ] Working memory
- [ ] Episodic memory
- [ ] Semantic memory interface
- [ ] Skill registry
- [ ] Skill versioning
- [ ] Provenance and retention

## Stage 6 — Human approval

- [ ] Approval request object
- [ ] Approval expiry
- [ ] Approval binding to target/state
- [ ] Approve/reject/cancel APIs
- [ ] Audit trail

## Stage 7 — Computer-use sandbox

- [ ] Browser environment adapter
- [ ] Observation interface
- [ ] Typed UI actions
- [ ] State revalidation
- [ ] Screenshot evidence
- [ ] Session isolation
- [ ] Credential broker interface

## Stage 8 — Long-running workers

- [ ] Durable queue
- [ ] Worker lease
- [ ] Heartbeat
- [ ] Resume after crash
- [ ] Scheduled triggers
- [ ] Event triggers
- [ ] Circuit breakers

## Stage 9 — Verification and evaluation

- [ ] Deterministic verifiers
- [ ] Independent verification
- [ ] Trajectory evaluator
- [ ] Regression suite
- [ ] Safety suite
- [ ] Prompt-injection suite
- [ ] Cost/latency benchmark

## Stage 10 — Controlled improvement

- [ ] Trajectory store
- [ ] Failure clustering
- [ ] Improvement hypothesis format
- [ ] Candidate harness change
- [ ] Sandbox evaluation
- [ ] Canary
- [ ] Rollback

## Definition of done

A stage is complete only when its implementation has:

1. executable code
2. unit/integration tests
3. failure tests
4. measurable metrics
5. documented security boundary
6. reproducible example
7. interview/system-design explanation

The capstone should grow incrementally. Do not introduce a framework merely to hide a missing primitive.
