from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class Episode:
    task_id:str; action:Any; outcome:Any; reward:float; verified:bool

class Environment:
    def __init__(self, transition:Callable[[Any,Any],Any], verifier:Callable[[Any,Any],bool]): self.transition,self.verifier=transition,verifier
    def step(self,state,action)->Episode:
        outcome=self.transition(state,action); ok=self.verifier(action,outcome)
        return Episode('synthetic',action,outcome,1.0 if ok else 0.0,ok)
