"""Small deterministic async LLM client used by the Module 2 labs."""
from __future__ import annotations
import asyncio
import random
import time
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    model: str

@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    latency_ms: float
    attempts: int

@dataclass(frozen=True)
class LLMConfig:
    timeout_s: float = 5.0
    max_attempts: int = 3
    concurrency: int = 10
    backoff_s: float = 0.05

class RetryableProviderError(Exception):
    """Synthetic transient provider failure for deterministic labs."""

class Provider(Protocol):
    async def generate(self, request: LLMRequest) -> str: ...

class AsyncLLMClient:
    def __init__(self, provider: Provider, config: LLMConfig = LLMConfig()):
        if config.max_attempts < 1 or config.concurrency < 1 or config.timeout_s <= 0:
            raise ValueError("invalid client configuration")
        self.provider = provider
        self.config = config
        self._sem = asyncio.Semaphore(config.concurrency)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        if not request.prompt.strip() or not request.model.strip():
            raise ValueError("prompt and model are required")
        started = time.perf_counter()
        attempts = 0
        async with self._sem:
            for attempt in range(1, self.config.max_attempts + 1):
                attempts = attempt
                try:
                    text = await asyncio.wait_for(self.provider.generate(request), self.config.timeout_s)
                    return LLMResponse(text=text, model=request.model,
                                       latency_ms=(time.perf_counter()-started)*1000,
                                       attempts=attempts)
                except asyncio.CancelledError:
                    raise
                except (RetryableProviderError, TimeoutError, asyncio.TimeoutError):
                    if attempt >= self.config.max_attempts:
                        raise
                    delay = random.uniform(0, self.config.backoff_s * (2 ** (attempt-1)))
                    await asyncio.sleep(delay)
        raise RuntimeError("unreachable")
