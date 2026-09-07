# Module 23 — MCP Fundamentals: Build an MCP Client

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
