# Module 24 — MCP Server: Build an Enterprise MCP Server

## Mission

Turn the Module 23 client boundary into a governed enterprise capability server. The server owns capability contracts and safe execution mechanics; the surrounding AegisAI control plane owns identity, authorization, approval, audit, budgets and verification.

## Architecture

```text
Agent / MCP Client
        |
   authentication
        |
   MCP Gateway
        |
 +------+-------+----------------+
 |      |       |                |
Tools Resources Prompts     Policy/Audit
 |      |       |                |
 +------+-------+----------------+
        |
   Enterprise APIs
```

## Learning outcomes

- Design an MCP server capability catalog.
- Build typed, deterministic tool handlers.
- Separate discovery from authorization.
- Enforce tenant boundaries at execution time.
- Handle lifecycle, versioning, timeouts and errors.
- Make side effects idempotent.
- Expose resources without leaking unrestricted data.
- Test malicious tool inputs and outputs.
- Instrument every request for Module 22 debugging.

## Server design principles

1. **Explicit contracts:** every tool has a stable schema.
2. **Least privilege:** expose the smallest useful capability.
3. **Fail closed:** invalid identity, arguments or tenant context means no execution.
4. **Side-effect discipline:** mutation requires idempotency and authorization.
5. **Untrusted outputs:** returned content cannot change policy.
6. **Version everything:** server, capability, schema and downstream dependency.
7. **Observe everything important:** request, decision, execution, result and error.

## Capability types

### Tools
Actions that execute code or cause side effects.

### Resources
Read-oriented contextual data. Resource URIs must still be authorized.

### Prompts
Reusable templates. Never treat a server prompt as a privileged system instruction.

## Detailed labs

### Lab 1 — Server manifest
Create a catalog with tools/resources/prompts and versions.

### Lab 2 — Tool contract
Implement typed validation and canonical argument serialization.

### Lab 3 — Read-only resource
Expose tenant-scoped documents through an authorized resource handler.

### Lab 4 — Mutation tool
Build an idempotent update operation with exact action identity.

### Lab 5 — Authentication boundary
Simulate authenticated principals and reject missing/invalid identity.

### Lab 6 — Authorization
Map principal roles and tenants to capability permissions.

### Lab 7 — Approval gate
Require a matching approval for high-risk mutation.

### Lab 8 — Rate/timeout budget
Prevent slow or abusive clients from consuming unlimited resources.

### Lab 9 — Audit and tracing
Emit correlation, causation, policy and execution events.

### Lab 10 — Schema evolution
Introduce v2 of a tool without silently breaking v1 clients.

### Lab 11 — Failure injection
Test downstream timeout, malformed dependency response, duplicate request and partial failure.

### Lab 12 — Security red team
Attempt cross-tenant access, argument injection, SSRF-like URL access and policy override through tool output.

### Lab 13 — Operational readiness
Implement health/readiness semantics, graceful shutdown and bounded concurrency.

### Lab 14 — Debugging integration
Feed server events into Module 22's distributed debugger and identify first failure.

### Lab 15 — Production review
Write a threat model, SLO, rollback plan and emergency capability-revocation procedure.

## Failure-first exercises

Break the server intentionally:

- remove a required argument;
- alter the schema version;
- replay a mutation;
- use another tenant ID;
- expire approval before execution;
- return malicious content;
- make the dependency hang;
- make the downstream API return a conflicting version;
- exceed rate limits;
- leak a secret through an error message.

For every failure, document **expected behavior, observed behavior, root cause and regression test**.

## Production metrics

- request success/error rate;
- p50/p95/p99 latency;
- active sessions;
- capability invocation volume;
- authorization-denial rate;
- approval rejection/expiry rate;
- duplicate mutation rate;
- downstream failure rate;
- tenant isolation violations;
- cost/resource consumption;
- trace completeness.

## Industry scenarios

**Banking:** account lookup and payment initiation separated into distinct capabilities with different approval requirements.

**Healthcare:** patient resources scoped by organization and purpose; mutation tools isolated behind stronger controls.

**Cybersecurity:** threat-intelligence reads separated from containment actions.

**Enterprise IT:** ticket reads available broadly while infrastructure mutation requires elevated role, approval and audit.

## Interview questions

1. What belongs inside an MCP server?
2. Where should authorization happen?
3. Why is capability discovery not authorization?
4. How do you make a mutation idempotent?
5. How should resource URIs be secured?
6. How do you evolve a tool schema safely?
7. What should happen on downstream timeout?
8. How do you prevent tool output from becoming privileged instructions?
9. How do you revoke a dangerous capability quickly?
10. How would you scale a server serving thousands of agents?
11. What belongs in the audit trail?
12. How would you debug a server-induced agent failure?

## System-design challenge

Design a regional MCP capability platform serving 50,000 agents and 5,000 enterprise tools. Include authentication, authorization, tenant isolation, capability registry, rate limits, idempotency, approvals, observability, versioning, failover and emergency revocation.

## Coding challenges

- capability registry;
- schema validator;
- principal/tenant authorizer;
- canonical action hash;
- idempotency store;
- approval checker;
- resource URI authorizer;
- retry classifier;
- audit correlator;
- schema compatibility checker.

## Mastery gate

Build a server with at least two read capabilities and one mutation capability. Demonstrate tenant isolation, typed validation, idempotency, approval, audit, timeout handling and a regression suite.

## Gold challenge

Connect Modules 18–23 to build **AegisAI Enterprise MCP Gateway** where every external capability crosses a visible security and observability boundary before execution.
