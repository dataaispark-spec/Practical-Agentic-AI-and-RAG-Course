from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Skill:
    name:str; version:str; confidence:float; status:str='candidate'

class SkillRegistry:
    def __init__(self): self._skills={}
    def register(self, skill:Skill): self._skills[(skill.name,skill.version)]=skill
    def promote(self,name,version,min_confidence=.9):
        key=(name,version); skill=self._skills[key]
        if skill.confidence < min_confidence: raise ValueError('confidence gate failed')
        promoted=Skill(skill.name,skill.version,skill.confidence,'trusted'); self._skills[key]=promoted; return promoted
    def get(self,name,version): return self._skills[(name,version)]
