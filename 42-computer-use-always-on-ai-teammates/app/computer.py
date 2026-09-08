from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass
class ComputerState:
    screen:str='home'; history:list[dict[str,Any]]=field(default_factory=list)

class ComputerPolicy:
    def __init__(self, allowed_actions:set[str], require_approval:set[str]|None=None): self.allowed_actions=allowed_actions; self.require_approval=require_approval or set()
    def authorize(self, action:str, approved=False)->bool:
        return action in self.allowed_actions and (action not in self.require_approval or approved)

class MockComputer:
    def __init__(self, policy:ComputerPolicy): self.policy=policy
    def act(self,state:ComputerState,action:str,args=None,approved=False):
        if not self.policy.authorize(action,approved): raise PermissionError('computer action denied')
        state.history.append({'action':action,'args':args or {}}); state.screen=f'after:{action}'; return state
