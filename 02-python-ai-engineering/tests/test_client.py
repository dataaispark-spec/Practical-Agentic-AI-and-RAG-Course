import asyncio
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1] / "labs" / "async_llm_client"
sys.path.insert(0, str(ROOT))

from client import AsyncLLMClient
from models import ClientConfig, LLMRequest
from provider import AIRateLimitError, AIValidationError, FakeProvider


@pytest.mark.asyncio
async def test_success():
    provider = FakeProvider(["success"])
    client = AsyncLLMClient(provider, ClientConfig(max_retries=0))
    result = await client.generate(LLMRequest("hello", "test-model"))
    assert result.text.startswith("fake response")
    assert result.attempts == 1


@pytest.mark.asyncio
async def test_rate_limit_retries_then_succeeds():
    provider = FakeProvider(["rate_limit", "success"])
    client = AsyncLLMClient(
        provider,
        ClientConfig(max_retries=1, base_backoff_seconds=0, max_backoff_seconds=0),
    )
    result = await client.generate(LLMRequest("hello", "test-model"))
    assert result.attempts == 2
    assert provider.calls == 2


@pytest.mark.asyncio
async def test_invalid_request_is_not_retried():
    provider = FakeProvider(["success"])
    client = AsyncLLMClient(provider, ClientConfig(max_retries=3))
    with pytest.raises(AIValidationError):
        await client.generate(LLMRequest("", "test-model"))
    assert provider.calls == 0


@pytest.mark.asyncio
async def test_cancellation_propagates():
    class SlowProvider:
        async def generate(self, request):
            await asyncio.sleep(10)

    client = AsyncLLMClient(
        SlowProvider(),
        ClientConfig(timeout_seconds=20, max_retries=0),
    )
    task = asyncio.create_task(client.generate(LLMRequest("hello", "test")))
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
