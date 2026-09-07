from collections.abc import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from .errors import AIProviderError, AIRateLimitError, AITimeoutError, AIValidationError
from .models import GenerateRequest
from .provider import FakeProvider
from .service import AIService

app = FastAPI(title="AegisAI Streaming API", version="0.1.0")
service = AIService(FakeProvider())


def error_response(request: Request, status_code: int, code: str, message: str) -> JSONResponse:
    request_id = request.headers.get("x-request-id", "generated-at-edge")
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}, "request_id": request_id},
    )


@app.exception_handler(AIValidationError)
async def validation_handler(request: Request, exc: AIValidationError):
    return error_response(request, 422, "invalid_request", str(exc))


@app.exception_handler(AIRateLimitError)
async def rate_limit_handler(request: Request, exc: AIRateLimitError):
    return error_response(request, 429, "upstream_rate_limit", str(exc))


@app.exception_handler(AITimeoutError)
async def timeout_handler(request: Request, exc: AITimeoutError):
    return error_response(request, 504, "upstream_timeout", str(exc))


@app.exception_handler(AIProviderError)
async def provider_handler(request: Request, exc: AIProviderError):
    return error_response(request, 502, "upstream_failure", str(exc))


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/generate")
async def generate(payload: GenerateRequest) -> dict[str, str]:
    result = await service.generate(payload)
    return {"text": result.text, "model": result.model, "request_id": result.request_id}


@app.post("/v1/generate/stream")
async def generate_stream(payload: GenerateRequest) -> StreamingResponse:
    async def events() -> AsyncIterator[str]:
        async for chunk in service.stream(payload):
            yield f'data: {{"type":"token","text":{chunk!r}}}\n\n'
        yield 'data: {"type":"done"}\n\n'

    return StreamingResponse(events(), media_type="text/event-stream")
