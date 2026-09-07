from dataclasses import dataclass


@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    model: str
    temperature: float = 0.0
    max_tokens: int = 512


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    latency_ms: float
    attempts: int
    input_tokens: int | None = None
    output_tokens: int | None = None


@dataclass(frozen=True)
class ClientConfig:
    timeout_seconds: float = 10.0
    max_retries: int = 2
    concurrency_limit: int = 10
    base_backoff_seconds: float = 0.1
    max_backoff_seconds: float = 2.0
