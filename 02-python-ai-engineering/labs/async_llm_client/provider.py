from typing import Protocol

from models import LLMRequest, LLMResponse


class AIClientError(Exception):
    pass


class AIValidationError(AIClientError):
    pass


class AIRateLimitError(AIClientError):
    pass


class AITimeoutError(AIClientError):
    pass


class AIProviderError(AIClientError):
    pass


class LLMProvider(Protocol):
    async def generate(self, request: LLMRequest) -> LLMResponse:
        ...


class FakeProvider:
    """Deterministic provider for tests and failure injection."""

    def __init__(self, outcomes: list[str]):
        self.outcomes = list(outcomes)
        self.calls = 0

    async def generate(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        outcome = self.outcomes.pop(0) if self.outcomes else "success"
        if outcome == "rate_limit":
            raise AIRateLimitError("simulated rate limit")
        if outcome == "timeout":
            raise AITimeoutError("simulated timeout")
        if outcome == "provider_error":
            raise AIProviderError("simulated provider failure")
        return LLMResponse(
            text=f"fake response: {request.prompt}",
            model=request.model,
            latency_ms=1.0,
            attempts=1,
        )
