# Module 23 — MCP Fundamentals


## Mission

Learn the protocol boundary between an agent and external capabilities. Build an educational MCP-style client from first principles before using an SDK.

**Mental model:** MCP is a capability/context interface; it does not replace authorization, policy, observability, budgets or verification.

## Learning outcomes

- Understand hosts, clients and servers.
- Discover tools, resources and prompts.
- Validate capability metadata before use.
- Construct typed tool calls.
- Handle malformed responses, timeouts and version mismatch.
- Preserve tenant and security context.
- Add approval and audit controls around MCP actions.
- Debug MCP interactions as distributed traces.

## Architecture

```text
AegisAI Agent
    |
    | MCP client
    v
+----------------+
| MCP transport  |
+----------------+
    |
    v
MCP server
  |-- tools
  |-- resources
  `-- prompts
```

The client is the trust-boundary adapter. Treat server-provided metadata and tool outputs as untrusted unless an explicit trust policy says otherwise.

## Core concepts

### Host
The application containing the agent experience.

### Client
The protocol participant that maintains a connection/session with a server and requests capabilities.

### Server
A process exposing capabilities through the protocol.

### Tool
An executable capability with a name, description and input contract.

### Resource
Addressable contextual data exposed by a server.

### Prompt
Reusable prompt/template capability exposed by a server.

## Capability discovery

Discovery should be explicit:

1. connect;
2. negotiate protocol/version capabilities;
3. enumerate available capabilities;
4. validate schemas;
5. map capabilities to internal policy;
6. expose only approved capabilities to the agent.

Do not blindly inject every discovered tool into an LLM prompt.

## Security model

MCP does not make a tool safe merely because it is standardized.

Apply:

- server identity/authentication;
- capability allowlists;
- least privilege;
- tenant binding;
- argument validation;
- egress controls;
- approval gates for high-impact actions;
- timeout/retry budgets;
- audit logging;
- output trust labeling;
- secret minimization.

## Labs

### Lab 1 — Capability registry
Create a local server manifest containing tools/resources/prompts.

### Lab 2 — Client discovery
Implement capability discovery and schema validation.

### Lab 3 — Typed tool call
Build a calculator/time/data tool request and validate arguments.

### Lab 4 — Malformed server
Inject an invalid response and ensure the client fails closed.

### Lab 5 — Timeout and retry
Simulate a slow server and apply bounded retry behavior.

### Lab 6 — Capability filtering
Expose only tools allowed by agent role and tenant.

### Lab 7 — Approval binding
Require exact approval for a high-impact tool action.

### Lab 8 — Tool poisoning
Return malicious instructions from a tool result and verify they remain data.

### Lab 9 — Audit
Record request, decision, result and correlation IDs.

### Lab 10 — Replay
Replay a recorded interaction using safe fixtures.

### Lab 11 — Multi-agent MCP
Connect supervisor and workers through separate capability sets.

### Lab 12 — Failure injection
Test disconnects, duplicate requests, stale sessions, schema drift and partial responses.

## Failure-first exercises

- server advertises a dangerous tool;
- tool description asks the model to ignore policy;
- result contains a fake system instruction;
- response schema changes;
- duplicate request creates a duplicate side effect;
- wrong tenant reaches a server;
- expired approval is replayed;
- server becomes slow;
- client retries a non-idempotent operation.

## Production checklist

Before deploying an MCP integration, answer:

- Which servers are trusted?
- Which capabilities are allowed?
- Who owns authorization?
- How are secrets handled?
- Which operations need approval?
- How are tenant boundaries enforced?
- How are tool calls traced?
- What is the retry/idempotency contract?
- How is server/schema versioning managed?
- How can access be revoked quickly?

## Industry scenarios

**Banking:** read account information through a narrowly scoped server while keeping transaction execution behind explicit policy.

**Healthcare:** expose approved clinical resources without allowing arbitrary external egress.

**Cybersecurity:** connect threat-intelligence tools while treating retrieved indicators as untrusted data.

**Enterprise IT:** provide ticketing and infrastructure tools with role-specific capabilities and approval gates.

## Interview bank

1. What problem does MCP solve?
2. Host vs client vs server?
3. Why discover capabilities dynamically?
4. Why is MCP not an authorization system?
5. How would you secure a remote MCP server?
6. How do you handle tool-result prompt injection?
7. How do you prevent duplicate side effects?
8. How should capability versioning work?
9. Where should tenant authorization live?
10. How would you observe MCP calls at scale?

## System-design challenge

Design a multi-tenant MCP gateway for 10,000 tools and 1,000 servers. Include discovery caching, capability policy, authentication, authorization, rate limits, approvals, tracing, schema/version management and emergency revocation.

## Coding challenges

- Capability manifest validator
- Tool-call schema validator
- MCP session state machine
- Retry classifier
- Idempotency layer
- Capability policy engine
- Tool-output trust wrapper
- Audit event correlator

## Mastery gate

Build a working client that discovers a server, filters capabilities through policy, performs typed calls, handles failures safely, records an auditable trace and refuses an unauthorized high-impact operation.

## Gold challenge

Integrate the client with Modules 18–22 so an MCP tool call flows through **security → policy → coordination → tracing → verification** before it can affect the outside world.

## Expanded long-form course chapter

This course is a practical engineering progression from deterministic software and LLM applications to retrieval, tools, stateful agents, distributed coordination, knowledge graphs, durable autonomy, verification, computer use, and controlled self-improvement. The governing idea is that an AI system becomes production-grade not by adding more model calls, but by adding explicit boundaries around probabilistic decisions. Throughout the 43 modules, the learner repeatedly asks: What is the goal? What state is authoritative? What evidence is available? What actions are permitted? What budget applies? What must be verified? What happens when a dependency fails? What must be observable and auditable? What evidence would justify changing the design?

The course uses the AegisAI mental model: Model + Harness + Environment + Tools + State + Policy + Budget + Verification. Retrieval is treated as a knowledge mechanism; an agent loop is treated as a decision-and-action mechanism; a harness is treated as the control plane around the model; and a verifier is treated as an independent check on outcomes. This distinction prevents a common engineering failure in which a prompt is asked to perform authorization, correctness checking, persistence, and business policy simultaneously.

Every module follows the same learning rhythm: Predict → Run → Observe → Explain → Break → Debug → Measure → Improve → Defend. The examples therefore emphasize observable mechanisms, explicit contracts, failure injection, metrics, and regression tests. The notebooks and applications are intended to work with deterministic fakes and synthetic data wherever possible, so that the learner can understand the mechanism before depending on a commercial provider.

## Module-specific learning contract

This expanded chapter deepens the repository canonical learning objectives for **Module 23: MCP Fundamentals**. The objective vocabulary is preserved: MCP client, host, client, server, discovery, and capability validation. Each concept is connected to architecture, implementation, failure analysis, evaluation, security, operations and system-design reasoning.

## First-principles concepts

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Architecture and control boundaries

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Mechanisms and implementation reasoning

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Industry scenarios and worked examples

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Failure-first engineering

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Experiments and measurement

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Security, governance and responsible operation

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Production design and operational readiness

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Debugging and incident analysis

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Exercises and independent practice

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## System-design review

### 1. Mcp Client

The first principle for MCP Fundamentals is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, MCP client should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Host

A practical way to learn MCP Fundamentals is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for host; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Client

In an enterprise setting, MCP Fundamentals rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. client becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Server

The failure-first perspective is especially important for MCP Fundamentals. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For server, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Discovery

Measurement should accompany every meaningful change to MCP Fundamentals. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For discovery, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Capability Validation

A useful architecture diagram for MCP Fundamentals separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For capability validation, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Mcp Client

Versioning is part of the technical design of MCP Fundamentals, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If MCP client changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Host

The final production question for MCP Fundamentals is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For host, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Assessment and mastery

### Question 1

Explain how you would design, implement, test, observe and defend **MCP client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 2

Explain how you would design, implement, test, observe and defend **host** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 3

Explain how you would design, implement, test, observe and defend **client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 4

Explain how you would design, implement, test, observe and defend **server** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 5

Explain how you would design, implement, test, observe and defend **discovery** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 6

Explain how you would design, implement, test, observe and defend **capability validation** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 7

Explain how you would design, implement, test, observe and defend **MCP client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 8

Explain how you would design, implement, test, observe and defend **host** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 9

Explain how you would design, implement, test, observe and defend **client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 10

Explain how you would design, implement, test, observe and defend **server** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 11

Explain how you would design, implement, test, observe and defend **discovery** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 12

Explain how you would design, implement, test, observe and defend **capability validation** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 13

Explain how you would design, implement, test, observe and defend **MCP client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 14

Explain how you would design, implement, test, observe and defend **host** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 15

Explain how you would design, implement, test, observe and defend **client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 16

Explain how you would design, implement, test, observe and defend **server** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 17

Explain how you would design, implement, test, observe and defend **discovery** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 18

Explain how you would design, implement, test, observe and defend **capability validation** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 19

Explain how you would design, implement, test, observe and defend **MCP client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 20

Explain how you would design, implement, test, observe and defend **host** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 21

Explain how you would design, implement, test, observe and defend **client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 22

Explain how you would design, implement, test, observe and defend **server** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 23

Explain how you would design, implement, test, observe and defend **discovery** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 24

Explain how you would design, implement, test, observe and defend **capability validation** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 25

Explain how you would design, implement, test, observe and defend **MCP client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 26

Explain how you would design, implement, test, observe and defend **host** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 27

Explain how you would design, implement, test, observe and defend **client** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 28

Explain how you would design, implement, test, observe and defend **server** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 29

Explain how you would design, implement, test, observe and defend **discovery** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 30

Explain how you would design, implement, test, observe and defend **capability validation** in a real MCP Fundamentals system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

## Mastery gate

Completion means being able to explain the mechanism from first principles, implement the smallest working version, deliberately break it, identify the first failing boundary from evidence, repair it, measure the repaired system against a baseline, and defend the resulting trade-offs. The learner should also explain when not to use the mechanism. Production expertise includes recognizing when a simpler deterministic solution is safer, cheaper and easier to operate.

## Deep case study 1: Mcp Client

Consider an enterprise workload in which MCP client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why MCP client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 2: Host

Consider an enterprise workload in which host is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why host cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 3: Client

Consider an enterprise workload in which client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 4: Server

Consider an enterprise workload in which server is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why server cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 5: Discovery

Consider an enterprise workload in which discovery is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why discovery cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 6: Capability Validation

Consider an enterprise workload in which capability validation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capability validation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 7: Mcp Client

Consider an enterprise workload in which MCP client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why MCP client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 8: Host

Consider an enterprise workload in which host is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why host cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 9: Client

Consider an enterprise workload in which client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 10: Server

Consider an enterprise workload in which server is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why server cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 11: Discovery

Consider an enterprise workload in which discovery is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why discovery cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 12: Capability Validation

Consider an enterprise workload in which capability validation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capability validation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 13: Mcp Client

Consider an enterprise workload in which MCP client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why MCP client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 14: Host

Consider an enterprise workload in which host is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why host cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 15: Client

Consider an enterprise workload in which client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 16: Server

Consider an enterprise workload in which server is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why server cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 17: Discovery

Consider an enterprise workload in which discovery is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why discovery cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 18: Capability Validation

Consider an enterprise workload in which capability validation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capability validation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 19: Mcp Client

Consider an enterprise workload in which MCP client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why MCP client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 20: Host

Consider an enterprise workload in which host is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why host cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 21: Client

Consider an enterprise workload in which client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 22: Server

Consider an enterprise workload in which server is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why server cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 23: Discovery

Consider an enterprise workload in which discovery is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why discovery cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 24: Capability Validation

Consider an enterprise workload in which capability validation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capability validation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 25: Mcp Client

Consider an enterprise workload in which MCP client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why MCP client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 26: Host

Consider an enterprise workload in which host is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why host cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 27: Client

Consider an enterprise workload in which client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 28: Server

Consider an enterprise workload in which server is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why server cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 29: Discovery

Consider an enterprise workload in which discovery is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why discovery cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 30: Capability Validation

Consider an enterprise workload in which capability validation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capability validation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 31: Mcp Client

Consider an enterprise workload in which MCP client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why MCP client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 32: Host

Consider an enterprise workload in which host is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why host cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 33: Client

Consider an enterprise workload in which client is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why client cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 34: Server

Consider an enterprise workload in which server is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why server cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.
