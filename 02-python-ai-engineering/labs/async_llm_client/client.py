import asyncio
import random
import time
from collections.abc import Awaitable, Callable

from models import ClientConfig, LLMRequest, LLMResponse
from provider import (
    AIRateLimitError,
    AITimeoutError,
    AIProviderError,
    AIValidationError,
    LLMProvider,
)


RETRYABLE = (AIRateLimitError, AITimeoutError, AIProviderError)


class AsyncLLMClient:
    def __init__(self, provider: LLMProvider, config: ClientConfig):
        if config.concurrency_limit < 1:
            raise ValueError("concurrency_limit must be >= 1")
        if config.max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        self.provider = provider
        self.config = config
        self.semaphore = asyncio.Semaphore(config.concurrency_limit)

    def _validate(self, request: LLMRequest) -> None:
        if not request.prompt.strip():
            raise AIValidationError("prompt must not be empty")
        if request.max_tokens <= 0:
            raise AIValidationError("max_tokens must be positive")
        if not 0 <= request.temperature <= 2:
            raise AIValidationError("temperature must be between 0 and 2")

    async def _sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        self._validate(request)
        async with self.semaphore:
            started = time.perf_counter()
            attempts = 0
            while True:
                attempts += 1
                try:
                    response = await asyncio.wait_for(
                        self.provider.generate(request),
                        timeout=self.config.timeout_seconds,
                    )
                    elapsed_ms = (time.perf_counter() - started) * 1000
                    return LLMResponse(
                        text=response.text,
                        model=response.model,
                        latency_ms=elapsed_ms,
                        attempts=attempts,
                        input_tokens=response.input_tokens,
                        output_tokens=response.output_tokens,
                    )
                except asyncio.CancelledError:
                    raise
                except RETRYABLE:
                    if attempts > self.config.max_retries:
                        raise
                    delay_cap = min(
                        self.config.max_backoff_seconds,
                        self.config.base_backoff_seconds * (2 ** (attempts - 1)),
                    )
                    await self._sleep(random.uniform(0, delay_cap))
