# Module 3 — FastAPI + Testing: Build a Streaming AI API

## Mission
Turn the Python AI client from Module 2 into a production-shaped HTTP service. The focus is not FastAPI syntax; it is **API contracts, validation, dependency boundaries, streaming, cancellation, errors, testing, and operational behavior**.

## Learning outcomes

By the end of this module you can:

1. Design typed HTTP contracts for AI requests and responses.
2. Separate API, application, provider, and infrastructure layers.
3. Implement synchronous and streaming endpoints.
4. Validate inputs and return predictable errors.
5. Propagate request cancellation.
6. Test AI APIs without real model calls.
7. Test streaming and failure paths.
8. Explain idempotency, timeouts, authentication boundaries, and rate limiting.
9. Measure API latency and error behavior.
10. Diagnose common production FastAPI failures.

## Architecture

```text
Client
  |
  v
FastAPI route
  |
  v
Request validation
  |
  v
Application service
  |
  v
LLMProvider protocol
  |
  +--> real provider
  +--> fake provider
  |
  v
Typed response / stream
  |
  v
Telemetry + error mapping
```

The route should not contain provider-specific business logic.

## API contract

### POST /v1/generate

Request:

```json
{
  "prompt": "Explain RAG in three sentences",
  "model": "demo-model",
  "max_tokens": 128
}
```

Response:

```json
{
  "text": "...",
  "model": "demo-model",
  "request_id": "req-123"
}
```

### POST /v1/generate/stream

Returns newline-delimited chunks. A production implementation should define a documented event format rather than relying on arbitrary text fragments.

Example event sequence:

```text
data: {"type":"token","text":"RAG"}

data: {"type":"token","text":" retrieves"}

data: {"type":"done"}
```

## Error contract

Do not expose provider exceptions directly. Map internal errors to stable API semantics:

| Internal condition | HTTP behavior |
|---|---|
| invalid request | 400/422 |
| authentication failure | 401 |
| forbidden operation | 403 |
| rate limit | 429 |
| upstream timeout | 504 |
| transient upstream failure | 502/503 |
| unexpected internal failure | 500 |

The exact mapping should be an explicit application decision and tested as a contract.

## Production boundary

```text
HTTP request
   |
   +-- authentication
   +-- authorization
   +-- request validation
   +-- correlation ID
   |
   v
Application service
   |
   +-- timeout/deadline
   +-- concurrency control
   +-- provider adapter
   |
   v
Response
   |
   +-- schema validation
   +-- telemetry
```

Authentication and authorization are not the same thing. A valid identity does not automatically have permission to perform every operation.

## Streaming engineering

Streaming changes the failure model because the response can fail after the client has already received useful data.

Test at least:

- empty prompt rejected before streaming
- first chunk arrives
- provider fails before first chunk
- provider fails after partial output
- client disconnects
- cancellation reaches the provider layer
- final `done` event is emitted exactly once

Do not claim a stream succeeded merely because its first token arrived.

## Testing pyramid

```text
             End-to-end
                 /\
                /  \
           API contract tests
              /      \
             /        \
       service/provider tests
          /              \
         /________________\
              unit tests
```

Use fake providers for deterministic unit and API tests. Reserve real provider tests for explicitly controlled integration environments.

## Lab — Streaming AI API

Build the service in `app/` with these components:

```text
app/
  main.py
  models.py
  service.py
  errors.py
  provider.py

tests/
  test_generate.py
  test_stream.py
```

Required behaviors:

1. typed request validation
2. dependency-injected provider
3. non-streaming endpoint
4. streaming endpoint
5. stable error mapping
6. correlation/request ID
7. deterministic fake provider
8. cancellation-safe async code

## Failure lab

### Failure 1 — Provider call inside the route

**Symptom:** every endpoint change requires editing provider-specific code.

**Fix:** inject an application service depending on a provider protocol.

### Failure 2 — Broad exception handler

**Symptom:** every failure becomes HTTP 500 and useful diagnosis disappears.

**Fix:** classify expected errors and preserve unexpected failures for telemetry.

### Failure 3 — Streaming success declared too early

**Symptom:** the client receives tokens but the provider fails before completion.

**Fix:** model stream lifecycle explicitly and emit a terminal event only after successful completion.

### Failure 4 — Cancellation swallowed

**Symptom:** disconnected clients still consume model work.

**Fix:** propagate `asyncio.CancelledError` rather than converting it into a normal error response.

### Failure 5 — Tests call the real provider

**Symptom:** tests are slow, expensive, flaky, and impossible offline.

**Fix:** dependency injection plus a deterministic fake provider.

## Industry challenge

Design an API for an enterprise assistant with:

- JWT/OIDC identity
- tenant isolation
- streaming responses
- 20-second overall deadline
- provider fallback
- request-level rate limiting
- audit correlation
- no sensitive prompt logging

Defend where each control lives.

## Interview bank

1. Why use FastAPI for AI services?
2. What belongs in a route vs service layer?
3. How do async endpoints improve I/O throughput?
4. What happens when an async endpoint blocks the event loop?
5. How do you test a streaming endpoint?
6. How do you propagate cancellation?
7. Why should provider exceptions be mapped?
8. How do you avoid real LLM calls in unit tests?
9. What is dependency injection buying you here?
10. How would you rate-limit a model endpoint?
11. How would you implement tenant isolation?
12. What should a request ID accomplish?
13. What belongs in structured logs?
14. How do you handle provider failure after partial streaming output?
15. How do you enforce an end-to-end deadline?
16. How would you design graceful degradation?
17. What metrics would you expose?
18. How do you prevent prompt data leakage through logs?
19. How do you version an AI API contract?
20. How do you distinguish 429 from 503?

## Mastery gate

You are ready for Module 4 when you can build and test an async FastAPI service with typed contracts, fake-provider injection, streaming, cancellation, stable error mapping, correlation IDs, and measurable latency/error behavior.

### Gold challenge

Break the service deliberately with provider timeout, rate limit, partial-stream failure, cancellation, malformed output, and invalid input. For every failure, produce:

```text
symptom -> trace evidence -> root cause -> control -> regression test
```
