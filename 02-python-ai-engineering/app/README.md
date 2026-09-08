# Module 02 application boundary

The executable reference implementation lives in `labs/async_llm_client/` so learners can inspect the implementation as a focused lab. This `app/` package is the canonical application boundary for tooling and future service integration.

## Contract

`AsyncLLMClient(provider, config).generate(request)` validates input, bounds concurrency, applies timeout/retry policy only to retryable provider failures, and returns measured latency/attempt metadata.

The lab implementation is intentionally provider-neutral and deterministic in tests; no API key is required for the course QA path.
