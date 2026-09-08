from dataclasses import dataclass

@dataclass(frozen=True)
class Proposal:
    subject: str
    relation: str
    object: str
    evidence: str
    confidence: float

def validate(p: Proposal, known: set[str], threshold: float=.8) -> bool:
    return bool(p.evidence) and p.subject in known and p.object in known and 0 <= p.confidence <= 1 and p.confidence >= threshold

def commit(proposals: list[Proposal], known: set[str]) -> list[Proposal]:
    accepted=[]
    seen=set()
    for p in proposals:
        key=(p.subject,p.relation,p.object,p.evidence)
        if key not in seen and validate(p,known): accepted.append(p); seen.add(key)
    return accepted
