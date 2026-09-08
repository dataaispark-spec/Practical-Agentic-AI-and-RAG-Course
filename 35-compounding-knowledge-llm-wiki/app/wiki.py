from dataclasses import dataclass

@dataclass(frozen=True)
class Claim:
    topic: str
    text: str
    source: str
    version: int = 1

class Wiki:
    def __init__(self): self.claims={}
    def upsert(self, claim: Claim):
        current=self.claims.get(claim.topic)
        if current and claim.source == current.source and claim.text == current.text: return current
        self.claims[claim.topic]=claim
        return claim
    def page(self, topic:str)->str:
        c=self.claims.get(topic)
        return f"{c.text} [source={c.source}; version={c.version}]" if c else "UNKNOWN"
