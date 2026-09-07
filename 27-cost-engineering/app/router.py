from __future__ import annotations

from dataclasses import dataclass
from math import inf


class BudgetExceeded(Exception):
    pass


@dataclass(frozen=True)
class Route:
    name: str
    quality: float
    latency_ms: float
    cost_usd: float
    risk: float = 0.0
    capabilities: frozenset[str] = frozenset()
    privacy: str = "standard"


@dataclass(frozen=True)
class Requirements:
    min_quality: float
    max_latency_ms: float
    max_cost_usd: float
    required_capabilities: frozenset[str] = frozenset()
    allowed_privacy: frozenset[str] = frozenset({"standard", "private"})


@dataclass
class Budget:
    max_cost_usd: float
    spent_usd: float = 0.0

    def reserve(self, amount: float) -> None:
        if self.spent_usd + amount > self.max_cost_usd:
            raise BudgetExceeded("budget exceeded")
        self.spent_usd += amount


def feasible(route: Route, req: Requirements) -> bool:
    return (
        route.quality >= req.min_quality
        and route.latency_ms <= req.max_latency_ms
        and route.cost_usd <= req.max_cost_usd
        and req.required_capabilities.issubset(route.capabilities)
        and route.privacy in req.allowed_privacy
    )


def choose(routes: list[Route], req: Requirements, *, quality_weight: float = 1.0, latency_weight: float = 0.001) -> Route:
    candidates = [r for r in routes if feasible(r, req)]
    if not candidates:
        raise BudgetExceeded("no route satisfies hard constraints")
    return min(candidates, key=lambda r: r.cost_usd - quality_weight * r.quality + latency_weight * r.latency_ms)


def cost_per_success(total_cost: float, successes: int) -> float:
    return total_cost / successes if successes else inf


def retry_amplification(attempts: int, base_cost: float) -> float:
    return max(0, attempts) * base_cost
