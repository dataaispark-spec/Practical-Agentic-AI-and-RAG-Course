from dataclasses import dataclass
from typing import Literal

Privacy = Literal["public", "internal", "regulated"]


@dataclass(frozen=True)
class ModelProfile:
    name: str
    provider: str
    max_context_tokens: int
    supports_tools: bool
    supports_json: bool
    privacy_classes: frozenset[Privacy]
    cost_per_1k_input: float
    cost_per_1k_output: float
    expected_latency_ms: int
    quality_score: float
    healthy: bool = True


@dataclass(frozen=True)
class ModelRequest:
    context_tokens: int = 0
    requires_tools: bool = False
    requires_json: bool = False
    max_latency_ms: int = 10_000
    max_cost_usd: float = 1.0
    privacy_class: Privacy = "public"
    quality_weight: float = 0.5


class NoCompatibleModel(RuntimeError):
    pass


def estimate_cost(model: ModelProfile, input_tokens: int, output_tokens: int) -> float:
    return (input_tokens / 1000) * model.cost_per_1k_input + (output_tokens / 1000) * model.cost_per_1k_output


def compatible(model: ModelProfile, request: ModelRequest) -> bool:
    if not model.healthy:
        return False
    if request.context_tokens > model.max_context_tokens:
        return False
    if request.requires_tools and not model.supports_tools:
        return False
    if request.requires_json and not model.supports_json:
        return False
    if request.privacy_class not in model.privacy_classes:
        return False
    if model.expected_latency_ms > request.max_latency_ms:
        return False
    if estimate_cost(model, request.context_tokens, 500) > request.max_cost_usd:
        return False
    return True


class ModelRouter:
    def __init__(self, models: list[ModelProfile]):
        self.models = tuple(models)

    def candidates(self, request: ModelRequest) -> list[ModelProfile]:
        return [m for m in self.models if compatible(m, request)]

    def route(self, request: ModelRequest) -> ModelProfile:
        candidates = self.candidates(request)
        if not candidates:
            raise NoCompatibleModel("no model satisfies hard requirements")

        def score(model: ModelProfile) -> tuple[float, int, str]:
            # Higher quality is better; lower latency is better. Cost is already a hard constraint.
            normalized_latency = model.expected_latency_ms / max(request.max_latency_ms, 1)
            value = request.quality_weight * model.quality_score - (1 - request.quality_weight) * normalized_latency
            return (-value, model.expected_latency_ms, model.name)

        return sorted(candidates, key=score)[0]
