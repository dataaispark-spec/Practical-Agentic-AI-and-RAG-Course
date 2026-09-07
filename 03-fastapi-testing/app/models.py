from dataclasses import dataclass


@dataclass(frozen=True)
class GenerateRequest:
    prompt: str
    model: str = "demo-model"
    max_tokens: int = 256

    def validate(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt must not be empty")
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")


@dataclass(frozen=True)
class GenerateResponse:
    text: str
    model: str
    request_id: str
