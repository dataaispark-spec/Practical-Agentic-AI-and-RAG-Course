import pytest

from app.router import ModelProfile, ModelRequest, ModelRouter, NoCompatibleModel


FAST = ModelProfile(
    name="fast", provider="a", max_context_tokens=32_000,
    supports_tools=True, supports_json=True,
    privacy_classes=frozenset({"public", "internal"}),
    cost_per_1k_input=0.001, cost_per_1k_output=0.004,
    expected_latency_ms=500, quality_score=0.80,
)

STRONG = ModelProfile(
    name="strong", provider="b", max_context_tokens=128_000,
    supports_tools=True, supports_json=True,
    privacy_classes=frozenset({"public", "internal"}),
    cost_per_1k_input=0.01, cost_per_1k_output=0.03,
    expected_latency_ms=1500, quality_score=0.95,
)

PRIVATE = ModelProfile(
    name="private", provider="c", max_context_tokens=64_000,
    supports_tools=False, supports_json=True,
    privacy_classes=frozenset({"regulated"}),
    cost_per_1k_input=0.02, cost_per_1k_output=0.04,
    expected_latency_ms=1800, quality_score=0.90,
)


def test_router_selects_compatible_high_value_model():
    selected = ModelRouter([FAST, STRONG]).route(ModelRequest(max_cost_usd=1.0))
    assert selected.name == "strong"


def test_privacy_is_hard_constraint():
    selected = ModelRouter([FAST, PRIVATE]).route(ModelRequest(privacy_class="regulated", max_cost_usd=1.0))
    assert selected.name == "private"


def test_unhealthy_model_is_not_selected():
    unhealthy = ModelProfile(**{**FAST.__dict__, "healthy": False})
    selected = ModelRouter([unhealthy, STRONG]).route(ModelRequest(max_cost_usd=1.0))
    assert selected.name == "strong"


def test_no_compatible_model_fails_closed():
    with pytest.raises(NoCompatibleModel):
        ModelRouter([PRIVATE]).route(ModelRequest(privacy_class="public"))


def test_tool_requirement_filters_non_tool_models():
    selected = ModelRouter([PRIVATE, FAST]).route(ModelRequest(requires_tools=True, max_cost_usd=1.0))
    assert selected.name == "fast"
