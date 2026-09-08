"""Structural QA for the canonical 43-module Agentic AI + RAG course."""
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

CANONICAL={
 31:'31-knowledge-engineering-graph-rag',32:'32-graph-engineering-temporal-knowledge',33:'33-agentic-knowledge-graph-construction',34:'34-graph-vector-hybrid-retrieval',35:'35-compounding-knowledge-llm-wiki',
 36:'31-loop-engineering',37:'32-harness-engineering',38:'33-long-running-autonomous-agents',39:'34-skills-memory-continual-harnesses',40:'35-environments-verifiers-agentic-rl',41:'36-recursive-self-improving-agents',42:'37-computer-use-always-on-ai-teammates',43:'38-frontier-agentic-rag-capstone'}

KEYWORDS={
 'theory':['theory','concept','mental model','mechanism'],'diagram':['diagram','architecture','data flow','control flow'],
 'industry':['industry','banking','healthcare','cybersecurity','manufacturing','enterprise','e-commerce','legal'],
 'failure':['failure','break','fault','injection','debug'],'metrics':['metric','latency','cost','Recall@K','success rate','evaluation'],
 'security':['security','authorization','tenant','injection','audit'],'challenge':['challenge','exercise','mastery'],
 'solution':['solution','reference','hint'],'interview':['interview','system design']}
NB={'objectives':['objective','learning goals'],'concept_map':['concept map'],'mechanism':['mechanism','first principles'],
 'build':['BUILD','guided'],'try':['TRY','TODO','exercise'],'break':['BREAK','failure','broken'],
 'measure':['measure','metric','evaluation'],'security':['security','misuse','attack'],'challenge':['challenge','mastery'],'solution':['solution','reference']}

def path_for(n:int)->Path|None:
    if n in CANONICAL: return ROOT/CANONICAL[n]
    matches=sorted(ROOT.glob(f'{n:02d}-*')); return matches[0] if matches else None

def text(p:Path)->str:
    try:return p.read_text(encoding='utf-8',errors='ignore')
    except OSError:return ''

def nb_text(p:Path)->str:
    try:d=json.loads(p.read_text(encoding='utf-8'))
    except Exception:return ''
    return '\n'.join(''.join(c.get('source',[])) if isinstance(c.get('source',[]),list) else str(c.get('source','')) for c in d.get('cells',[]))

def score(n:int)->dict:
    p=path_for(n)
    if p is None:return {'module':n,'status':'MISSING','score':0,'missing':['module directory']}
    r=text(p/'README.md'); nbs=list((p/'notebooks').glob('*.ipynb')) if (p/'notebooks').exists() else []
    nt='\n'.join(nb_text(x) for x in nbs); alltext=r+'\n'+nt
    ev={k:any(x.lower() in alltext.lower() for x in v) for k,v in KEYWORDS.items()}
    ne={k:any(x.lower() in nt.lower() for x in v) for k,v in NB.items()}
    art={'readme':(p/'README.md').exists(),'notebook':bool(nbs),'tests':bool(list(p.rglob('test_*.py'))),'app':(p/'app').exists()}
    missing=[k for k,v in ev.items() if not v]+['notebook:'+k for k,v in ne.items() if not v]+[k for k,v in art.items() if not v]
    return {'module':n,'status':'COMPLETE' if not missing else 'UPGRADE','score':sum(ev.values())+sum(ne.values())+sum(art.values()),'missing':missing,'path':str(p.relative_to(ROOT))}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--strict',action='store_true'); a=ap.parse_args()
    results=[score(i) for i in range(1,44)]; complete=sum(x['status']=='COMPLETE' for x in results)
    print('Agentic AI + RAG Course — canonical 43-module structural QA')
    print('='*60)
    for x in results:
        print(f"M{x['module']:02d}: {x['status']:<8} score={x['score']:02d} path={x.get('path','-')}")
        if x['missing']: print('  gaps:',', '.join(x['missing'][:8]))
    print('='*60); print(f'Complete: {complete}/43')
    print('Canonical M31–M35 are graph modules; M36–M43 map to preserved frontier implementation assets.')
    return 0 if (complete==43 or not a.strict) else 1

if __name__=='__main__': raise SystemExit(main())
