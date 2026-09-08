from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class Status(str, Enum): CREATED='created'; RUNNING='running'; WAITING='waiting'; COMPLETED='completed'; FAILED='failed'; CANCELLED='cancelled'
@dataclass
class DurableJob:
    job_id:str; goal:str; status:Status=Status.CREATED; checkpoint:int=0; effects:set[str]=field(default_factory=set); history:list[Any]=field(default_factory=list)

class DurableWorker:
    def __init__(self, effect:Callable[[str], Any]): self.effect=effect
    def run(self, job:DurableJob, steps:int=5)->DurableJob:
        if job.status is Status.CANCELLED: return job
        job.status=Status.RUNNING
        for i in range(job.checkpoint, steps):
            key=f'{job.job_id}:{i}'
            if key in job.effects: continue
            result=self.effect(key); job.effects.add(key); job.history.append(result); job.checkpoint=i+1
        job.status=Status.COMPLETED; return job
