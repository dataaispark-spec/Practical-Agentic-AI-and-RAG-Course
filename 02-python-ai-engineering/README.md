# Module 2 — Python for AI Engineering

## Module purpose

This module turns Python knowledge into **production AI engineering capability**. The goal is not to learn Python syntax in isolation; it is to build reliable asynchronous model clients, typed contracts, retries, timeouts, streaming, concurrency controls, configuration, testing seams, and measurable failure handling.

The learner builds a reusable **Production Async LLM Client** that becomes infrastructure for later RAG and agent modules.

## Source curriculum alignment

This module is the practical engineering expansion of the Python/software-engineering portion of the source IITM Pravartak curriculum. The source curriculum remains authoritative for its original scope and sequencing. The material below adds implementation depth, failure labs, production patterns, and interview preparation.

## Learning outcomes

By the end, you can:

1. Structure Python AI projects for maintainability.
2. Use type hints, dataclasses, protocols, exceptions, and validation as engineering contracts.
3. Explain synchronous vs asynchronous execution and choose appropriately.
4. Implement bounded concurrency for model/API calls.
5. Build retries with exponential backoff without creating retry storms.
6. Apply timeouts, cancellation, circuit-breaking concepts, and graceful degradation.
7. Stream model responses safely.
8. Separate provider-specific code from application logic.
9. Test AI infrastructure deterministically using fake providers.
10. Measure latency, failures, retries, concurrency, and estimated cost.
11. Debug production-style async failures.
12. Defend Python architecture choices in an engineering interview.

---

# 1. The real problem: AI code fails at the boundaries

A demo often looks like:

```python
response = client.generate("Explain RAG")
print(response)
```

Production code has a much larger contract:

```text
Application
   |
   v
Typed request
   |
   v
Policy / validation
   |
   v
Provider adapter
   |
   +---- timeout
   +---- retry budget
   +---- concurrency limit
   +---- cancellation
   +---- telemetry
   |
   v
Typed response
   |
   v
Application
```

The engineering question is not merely **“Can Python call an LLM?”**. It is:

> Can thousands of calls execute predictably when providers are slow, unavailable, rate-limited, malformed, expensive, or partially failing?

---

# 2. Python architecture for AI systems

A useful project boundary is:

```text
02-python-ai-engineering/
├── README.md
├── labs/
│   └── async_llm_client/
│       ├── client.py
│       ├── models.py
│       ├── provider.py
│       ├── retry.py
│       └── metrics.py
├── exercises/
├── solutions/
├── tests/
└── interview/
```

Keep business logic independent from a specific model vendor:

```text
Application code
      |
      v
LLM interface / Protocol
      |
      +-------- Provider A adapter
      |
      +-------- Provider B adapter
      |
      +-------- Fake provider for tests
```

This is dependency inversion applied to AI infrastructure.

---

# 3. Type hints are executable design documentation

A model request should have a contract.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    model: str
    temperature: float = 0.0
    max_tokens: int = 512
```

A response should also have a contract:

```python
@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    latency_ms: float
    input_tokens: int | None = None
    output_tokens: int | None = None
```

Why this matters:

- invalid inputs become visible early
- provider adapters have a common interface
- tests can construct deterministic objects
- refactoring becomes safer
- observability has known fields

Do not confuse type hints with runtime validation. A type annotation does not automatically reject bad external data.

---

# 4. Protocols: isolate provider dependencies

```python
from typing import Protocol


class LLMProvider(Protocol):
    async def generate(self, request: LLMRequest) -> LLMResponse:
        ...
```

The application depends on the protocol rather than a vendor SDK.

```text
                 +------------------+
                 | Application      |
                 +--------+---------+
                          |
                          v
                  +---------------+
                  | LLMProvider   |
                  | Protocol      |
                  +-------+-------+
                          |
             +------------+------------+
             |                         |
             v                         v
       Real provider              Fake provider
```

This makes the system testable without making real network calls.

---

# 5. Async Python: what problem are we solving?

AI applications frequently spend substantial time waiting on I/O:

- model APIs
- vector databases
- databases
- object storage
- HTTP services
- telemetry endpoints

For I/O-bound workloads, asynchronous execution can improve throughput by allowing other work to proceed while one request waits.

### Mental model

Synchronous:

```text
request A ---- wait ---- response
request B                    ---- wait ---- response
```

Asynchronous:

```text
request A ---- wait -------- response
request B    ---- wait -------- response
request C       ---- wait ----- response
```

Async is not magic parallel CPU execution. It is primarily a way to manage waiting efficiently.

---

# 6. Bounded concurrency

A dangerous implementation launches unlimited requests:

```python
await asyncio.gather(*(client.generate(r) for r in requests))
```

For a small list this may be fine. At production scale it can overload:

- your process
- the provider
- connection pools
- downstream systems
- rate limits
- budgets

Use a semaphore or a worker pool:

```python
import asyncio


async def run_bounded(requests, worker, limit: int = 10):
    semaphore = asyncio.Semaphore(limit)

    async def one(request):
        async with semaphore:
            return await worker(request)

    return await asyncio.gather(*(one(r) for r in requests))
```

### Engineering principle

**Concurrency is a resource budget, not merely a performance setting.**

---

# 7. Timeouts are mandatory

Every network operation needs a bounded waiting time.

```python
import asyncio


async def with_timeout(coro, timeout_seconds: float):
    return await asyncio.wait_for(coro, timeout=timeout_seconds)
```

In production, prefer the timeout primitives supported by your HTTP/client stack and propagate cancellation correctly.

A timeout should become an explicit application outcome:

```text
Provider call
   |
   +-- success --> response
   |
   +-- timeout --> retry/fallback/fail fast
```

Do not allow a hung upstream request to consume a worker indefinitely.

---

# 8. Retries: useful, dangerous, measurable

Transient failures happen:

- HTTP 429
- temporary 5xx responses
- connection resets
- provider overload

Retrying every exception is a bug.

A reasonable policy distinguishes:

```text
Error
 |
 +-- validation error ----------> fail immediately
 +-- authentication error -------> fail / alert
 +-- authorization error --------> fail / alert
 +-- deterministic bad request --> fail immediately
 +-- transient provider error ---> bounded retry
 +-- timeout --------------------> bounded retry/fallback
```

### Exponential backoff

A simplified schedule:

```text
attempt 1: immediate
attempt 2: ~0.5 s
attempt 3: ~1.0 s
attempt 4: ~2.0 s
```

Add jitter so many clients do not retry simultaneously.

A conceptual formula is:

```text
sleep = random(0, min(max_delay, base * 2^attempt))
```

Retries require a **total attempt budget** and should be observable.

---

# 9. Retry storms and the hidden multiplication problem

Suppose:

- 100 requests arrive
- each has 3 model calls
- each call retries twice

Worst-case upstream attempts can approach:

```text
100 × 3 × 3 = 900 attempts
```

A failure can therefore amplify load.

This is why production AI systems need:

- bounded retries
- concurrency limits
- provider rate awareness
- backoff + jitter
- circuit-breaking/degradation strategies
- budget controls

---

# 10. Error taxonomy

Define errors that the application can reason about.

```python
class AIClientError(Exception):
    """Base class for client failures."""


class AIValidationError(AIClientError):
    pass


class AIAuthenticationError(AIClientError):
    pass


class AIRateLimitError(AIClientError):
    pass


class AITimeoutError(AIClientError):
    pass


class AIProviderError(AIClientError):
    pass
```

Avoid returning strings such as `"something went wrong"`. Errors are part of the API contract.

---

# 11. Streaming is a product behavior, not a transport trick

For long responses, streaming can reduce time-to-first-token and improve perceived responsiveness.

```text
Request
  |
  v
Provider
  |
  +--> token/chunk 1
  +--> token/chunk 2
  +--> token/chunk 3
  +--> ...
  |
  v
Completed response
```

Production streaming must handle:

- client disconnects
- provider errors halfway through
- partial output
- cancellation
- malformed chunks
- telemetry completion

Never assume a stream always reaches a clean final event.

---

# 12. Cancellation and client disconnects

Imagine a user closes the browser after 100 ms while the model continues generating for 20 seconds.

If the server does not propagate cancellation, you may still pay for work the user no longer wants.

Design for:

```text
Client disconnect
      |
      v
Request cancellation
      |
      v
Cancel provider operation when safe
      |
      v
Record outcome + cost
```

Cancellation is especially important for agents because one request can contain many sequential tool/model calls.

---

# 13. Configuration and secrets

Never hard-code credentials:

```python
# Bad
API_KEY = "sk-secret-value"
```

Use environment/configuration boundaries:

```python
import os

API_KEY = os.environ["LLM_API_KEY"]
```

For production systems, use a proper secret-management mechanism and rotate credentials.

Configuration should separate:

- provider endpoint
- model name
- timeout
- maximum retries
- concurrency limit
- token budget
- feature flags

Code should not need modification merely to change an operational parameter.

---

# 14. Observability contract

Every model request should ideally produce structured telemetry such as:

```json
{
  "request_id": "req-123",
  "provider": "example",
  "model": "model-x",
  "latency_ms": 842,
  "attempts": 2,
  "status": "success",
  "input_tokens": 500,
  "output_tokens": 180
}
```

Do **not** log secrets, API keys, sensitive prompts, or personal data indiscriminately.

Core metrics:

| Metric | Why |
|---|---|
| request count | traffic |
| success/error rate | reliability |
| p50/p95/p99 latency | user experience |
| timeout rate | upstream health |
| retry count | instability |
| active concurrency | resource pressure |
| tokens | usage |
| estimated cost | economics |
| cancellation rate | wasted work / UX |

---

# 15. Cost engineering

A rough task cost model is:

```text
cost/task ≈ input_tokens × input_price
          + output_tokens × output_price
          + tool/API costs
          + retry overhead
```

Do not optimize only model price. A cheaper model that requires more retries or produces failed tasks can be more expensive at the product level.

A better business metric is often:

```text
cost per successful task
```

rather than merely cost per request.

---

# 16. Production Async LLM Client — build it

## Target interface

```python
client = AsyncLLMClient(provider, config)
response = await client.generate(request)
```

Required behavior:

1. validate the request
2. enforce timeout
3. enforce concurrency limit
4. classify provider errors
5. retry only retryable failures
6. use exponential backoff + jitter
7. return a typed response
8. emit metrics
9. preserve cancellation
10. never expose secrets through exceptions/logging

## Suggested implementation sequence

### Step 1 — models
Create request/response/config dataclasses.

### Step 2 — provider protocol
Define `generate()` and a streaming interface.

### Step 3 — fake provider
Create a deterministic provider that can simulate success, timeout, rate limiting, and provider failure.

### Step 4 — client
Implement validation, semaphore, timeout, retries, and metrics.

### Step 5 — tests
Test success and every failure path.

### Step 6 — benchmark
Run 1, 10, 100, and 500 logical requests with different concurrency limits.

---

# 17. Industry exercise set

## Exercise A — Batch summarization

You must summarize 10,000 documents overnight.

Constraints:

- provider rate limit: 100 requests/minute
- p95 provider latency: 2 seconds
- maximum worker concurrency: 20
- transient failure rate: 3%

Design:

- concurrency strategy
- retry policy
- queue behavior
- timeout
- checkpointing
- idempotency
- metrics

## Exercise B — Interactive support assistant

Target:

- time-to-first-token under 1.5 s
- p95 completion under 8 s
- graceful provider degradation

Explain when streaming is useful and what happens if the provider fails after partial output.

## Exercise C — Multi-provider fallback

Provider A is preferred; Provider B is fallback.

Define exactly which failures trigger fallback and which must fail immediately.

---

# 18. Failure lab

## Failure 1 — Unlimited gather

**Symptom:** 2,000 concurrent requests cause rate limits and memory pressure.

**Investigation:** inspect active tasks, provider responses, and event-loop behavior.

**Fix:** bounded concurrency plus provider-aware rate limiting.

## Failure 2 — Retry everything

**Symptom:** invalid requests generate repeated failures and increased cost.

**Fix:** classify errors before retrying.

## Failure 3 — Retry storm

**Symptom:** provider outage causes traffic amplification.

**Fix:** exponential backoff, jitter, retry budget, concurrency limits, and degradation.

## Failure 4 — Missing timeout

**Symptom:** workers remain occupied during upstream hangs.

**Fix:** explicit deadline propagation.

## Failure 5 — Swallowed cancellation

**Symptom:** users disconnect but model work continues.

**Fix:** propagate `CancelledError` correctly; do not catch broad exceptions and accidentally convert cancellation into a normal failure.

## Failure 6 — Provider lock-in

**Symptom:** application logic is deeply coupled to one SDK.

**Fix:** provider protocol + adapter boundary.

---

# 19. Debugging method

When an async AI service is slow, do not immediately increase worker count.

Trace the critical path:

```text
request queue
   |
   v
wait for semaphore
   |
   v
provider connection
   |
   v
provider processing
   |
   v
stream / response handling
   |
   v
post-processing
```

Measure each segment.

### Example diagnosis

**Symptom:** p95 increased from 4 s to 12 s.

**Evidence:** provider latency remains 3 s, but semaphore wait is 7 s.

**Hypothesis:** concurrency is too low for current traffic.

**Experiment:** raise concurrency from 10 to 20 under a controlled load test.

**Caution:** verify provider rate limits before increasing further.

---

# 20. Mastery gate

You pass Module 2 only when you can:

- implement a typed async client without copying a framework abstraction blindly
- explain the Python event loop at a practical level
- bound concurrency
- implement safe retry classification
- add timeout and cancellation handling
- stream partial output
- write deterministic tests with a fake provider
- diagnose a latency regression using measurements
- calculate retry amplification and approximate cost
- explain why provider adapters matter

### Gold-standard challenge

Build a client that survives a test workload containing:

```text
60% success
15% rate limits
10% timeouts
10% provider errors
5% invalid requests
```

It must:

- never retry invalid requests
- never exceed the configured concurrency
- cap attempts
- preserve cancellation
- report attempts and latency
- produce deterministic test results

---

# 21. Interview bank

## Foundations

1. What is the difference between concurrency and parallelism?
2. Why is async useful for AI applications?
3. What is an event loop?
4. What is a coroutine?
5. What problem does a semaphore solve?
6. Why should model calls have timeouts?
7. Why should exceptions be typed?
8. What is dependency inversion?
9. Why use a protocol/interface around an LLM provider?
10. Why is a fake provider useful in tests?

## Intermediate

11. How does exponential backoff work?
12. Why add jitter?
13. Which failures should not be retried?
14. How can retries amplify an outage?
15. What is graceful degradation?
16. How would you implement provider fallback?
17. What is cancellation in asyncio?
18. Why can broad exception handling be dangerous in async code?
19. What should you measure for an LLM client?
20. Why is cost per successful task more useful than cost per request?

## Advanced

21. Design a rate-aware async client for a provider limited to 100 requests/minute.
22. How would you prevent 10,000 requests from creating 10,000 active coroutines?
23. How would you debug rising p99 latency with normal provider latency?
24. How would you make retries idempotent?
25. How do you propagate a request deadline across multiple downstream calls?
26. Design a multi-provider failover policy.
27. How would you test a timeout without waiting for a real timeout?
28. What happens if a provider fails halfway through a stream?
29. How would you prevent secrets from appearing in logs?
30. How would you benchmark different concurrency limits fairly?

---

# 22. Coding challenges

### Challenge 1
Implement a bounded async map that preserves input ordering.

### Challenge 2
Implement retry logic with exponential backoff and jitter using an injectable sleep function for deterministic tests.

### Challenge 3
Implement a token/cost accumulator for requests and retries.

### Challenge 4
Implement a provider fallback chain with explicit retryable exception classes.

### Challenge 5
Implement a streaming adapter that converts provider-specific chunks into a common async iterator.

---

# 23. System design challenge

> Design a Python service that processes 1 million AI requests/day across multiple model providers, supports streaming for interactive traffic, batch execution for offline jobs, provider failover, cost limits, and complete request tracing.

Your answer must cover:

1. API boundary
2. async execution model
3. queues/workers
4. concurrency limits
5. rate limiting
6. retry policy
7. provider abstraction
8. streaming
9. cancellation
10. observability
11. cost controls
12. testing strategy
13. deployment/scaling
14. failure recovery

---

# 24. Deliverables

By the end of this module the repository should contain:

```text
02-python-ai-engineering/
├── README.md
├── labs/async_llm_client/
├── exercises/
├── solutions/
├── tests/
└── interview/
```

The module is intentionally designed to become a dependency for later modules rather than a disposable exercise.
