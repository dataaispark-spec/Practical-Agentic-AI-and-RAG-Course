import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass

from .errors import AIProviderError, AITimeoutError, AIRateLimitError
from .models import GenerateRequest


class LLMProvider:
    async def generate(self, request: GenerateRequest) -> str:
        raise NotImplementedError

    async def stream(self, request: GenerateRequest) -> AsyncIterator[str]:
        raise NotImplementedError


@dataclass
class FakeProvider(LLMProvider):
    response: str = "This is a deterministic demo response."
    fail_mode: str | None = None
    delay_seconds: float = 0.0

    async def _check(self) -> None:
        if self.delay_seconds:
            await asyncio.sleep(self.delay_seconds)
        if self.fail_mode == "timeout":
            raise AITimeoutError("provider timed out")
        if self.fail_mode == "rate_limit":
            raise AIRateLimitError("provider rate limit")
        if self.fail_mode == "provider":
            raise AIProviderError("provider failure")

    async def generate(self, request: GenerateRequest) -> str:
        await self._check()
        return self.response

    async def stream(self, request: GenerateRequest) -> AsyncIterator[str]:
        await self._check()
        for chunk in self.response.split():
            await asyncio.sleep(0)
            yield chunk + " "
