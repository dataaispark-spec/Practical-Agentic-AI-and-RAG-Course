from dataclasses import dataclass
from enum import Enum


class Risk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class Requirements:
    needs_generation: bool
    needs_knowledge: bool
    needs_actions: bool
    roles: int = 1
    risk: Risk = Risk.LOW
    human_approval: bool = False

    def __post_init__(self) -> None:
        if self.roles < 1:
            raise ValueError("roles must be >= 1")
