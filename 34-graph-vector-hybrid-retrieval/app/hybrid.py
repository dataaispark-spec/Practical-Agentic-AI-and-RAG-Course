from dataclasses import dataclass

@dataclass(frozen=True)
class Hit:
    item_id: str
    score: float

def rrf(*rankings: list[str], k: int = 60) -> list[Hit]:
    scores={}
    for ranking in rankings:
        for rank,item in enumerate(ranking,1): scores[item]=scores.get(item,0)+1/(k+rank)
    return [Hit(i,s) for i,s in sorted(scores.items(), key=lambda x:(-x[1],x[0]))]

def hybrid(graph_ids:list[str], vector_ids:list[str], top_k:int=5)->list[Hit]:
    return rrf(graph_ids,vector_ids)[:top_k]
