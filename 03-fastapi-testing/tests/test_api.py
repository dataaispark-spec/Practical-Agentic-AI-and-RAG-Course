import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from app.errors import AITimeoutError
from app.main import app, service
from app.provider import FakeProvider


@pytest.fixture(autouse=True)
def reset_provider():
    service.provider = FakeProvider(response="hello world")
    yield


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_generate_returns_typed_contract():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/v1/generate", json={"prompt": "hi", "model": "demo-model"})
    assert response.status_code == 200
    body = response.json()
    assert body["text"] == "hello world"
    assert body["model"] == "demo-model"
    assert body["request_id"]


@pytest.mark.asyncio
async def test_invalid_prompt_is_rejected():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/v1/generate", json={"prompt": "   "})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"


@pytest.mark.asyncio
async def test_provider_timeout_maps_to_gateway_timeout():
    service.provider = FakeProvider(fail_mode="timeout")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/v1/generate", json={"prompt": "hi"})
    assert response.status_code == 504


@pytest.mark.asyncio
async def test_stream_emits_terminal_done_event():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/v1/generate/stream", json={"prompt": "hi"})
    assert response.status_code == 200
    assert "type" in response.text
    assert "done" in response.text


@pytest.mark.asyncio
async def test_service_preserves_cancellation():
    class SlowProvider(FakeProvider):
        async def generate(self, request):
            await asyncio.sleep(10)
            return "never"

    service.provider = SlowProvider()
    task = asyncio.create_task(service.generate(__import__("app.models", fromlist=["GenerateRequest"]).GenerateRequest("hi")))
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
