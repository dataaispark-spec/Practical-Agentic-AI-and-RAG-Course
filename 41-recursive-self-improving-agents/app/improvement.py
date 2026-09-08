from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Candidate:
    candidate_id:str; version:str; artifact_hash:str; metrics:dict[str,float]

@dataclass(frozen=True)
class PromotionDecision:
    candidate_id:str; promoted:bool; reasons:tuple[str,...]

class ImprovementEngine:
    """Bounded experiment engine. The candidate cannot mutate the evaluator or promote itself."""
    def __init__(self, evaluator:Callable[[Candidate],dict[str,float]], max_experiments=3, min_success_gain=.02, max_cost_delta=.02):
        self.evaluator=evaluator; self.max_experiments=max_experiments; self.min_success_gain=min_success_gain; self.max_cost_delta=max_cost_delta; self.baseline=None; self.history=[]
    def set_baseline(self, metrics:dict[str,float]): self.baseline=dict(metrics)
    def evaluate(self,candidate:Candidate)->PromotionDecision:
        if self.baseline is None: raise RuntimeError('baseline required')
        if len(self.history)>=self.max_experiments: return PromotionDecision(candidate.candidate_id,False,('experiment_budget_exceeded',))
        observed=self.evaluator(candidate); self.history.append((candidate,observed))
        reasons=[]
        if observed.get('success',0)-self.baseline.get('success',0) < self.min_success_gain: reasons.append('insufficient_success_gain')
        if observed.get('safety',1) < self.baseline.get('safety',1): reasons.append('safety_regression')
        if observed.get('cost',0)-self.baseline.get('cost',0) > self.max_cost_delta: reasons.append('cost_regression')
        return PromotionDecision(candidate.candidate_id,not reasons,tuple(reasons))
