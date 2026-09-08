"""Deterministic resource budgets for agent runs."""

from dataclasses import dataclass


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class Budget:
    max_steps: int = 20
    max_tokens: int = 20_000
    max_tool_calls: int = 30
    max_cost_usd: float = 5.0
    steps: int = 0
    tokens: int = 0
    tool_calls: int = 0
    cost_usd: float = 0.0

    def consume_step(self, amount: int = 1) -> None:
        self.steps += amount
        if self.steps > self.max_steps:
            raise BudgetExceeded("step budget exceeded")

    def consume_tokens(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("token usage cannot be negative")
        self.tokens += amount
        if self.tokens > self.max_tokens:
            raise BudgetExceeded("token budget exceeded")

    def consume_tool_call(self, amount: int = 1) -> None:
        self.tool_calls += amount
        if self.tool_calls > self.max_tool_calls:
            raise BudgetExceeded("tool-call budget exceeded")

    def consume_cost(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("cost cannot be negative")
        self.cost_usd += amount
        if self.cost_usd > self.max_cost_usd:
            raise BudgetExceeded("cost budget exceeded")
