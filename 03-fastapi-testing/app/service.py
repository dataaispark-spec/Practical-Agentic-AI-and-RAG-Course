import asyncio
import uuid
from collections.abc import AsyncIterator

from .errors import AIProviderError, AIRateLimitError, AITimeoutError, AIValidationError
from .models import GenerateRequest, GenerateResponse
from .provider import LLMProvider


class AIService:
    def __init__(self, provider: LLMProvider, timeout_seconds: float = 20.0):
        self.provider = provider
        self.timeout_seconds = timeout_seconds

    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        try:
            request.validate()
        except ValueError as exc:
            raise AIValidationError(str(exc)) from exc

        request_id = str(uuid.uuid4())
        try:
            text = await asyncio.wait_for(
                self.provider.generate(request), timeout=self.timeout_seconds
            )
        except asyncio.CancelledError:
            raise
        except (AITimeoutError, AIRateLimitError, AIProviderError):
            raise
        except asyncio.TimeoutError as exc:
            raise AITimeoutError("AI provider deadline exceeded") from exc
        except Exception as exc:
            raise AIProviderError("unexpected provider failure") from exc
        return GenerateResponse(text=text, model=request.model, request_id=request_id)

    async def stream(self, request: GenerateRequest) -> AsyncIterator[str]:
        try:
            request.validate()
        except ValueError as exc:
            raise AIValidationError(str(exc)) from exc

        try:
            async with asyncio.timeout(self.timeout_seconds):
                async for chunk in self.provider.stream(request):
                    yield chunk
        except asyncio.CancelledError:
            raise
        except (AITimeoutError, AIRateLimitError, AIProviderError):
            raise
        except TimeoutError as exc:
            raise AITimeoutError("AI stream deadline exceeded") from exc
        except Exception as exc:
            raise AIProviderError("unexpected streaming failure") from exc
