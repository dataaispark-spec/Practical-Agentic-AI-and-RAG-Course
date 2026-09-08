"""Structural and pedagogical QA for the canonical 43-module Agentic AI + RAG course.

Strict mode is intentionally a structural gate: it verifies that every canonical
module has the expected reusable learning artifacts. Content coverage is still
reported as an upgrade backlog and is never silently treated as complete.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

CANONICAL={
 6:'06-rag-from-first-principles',
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

# Structural artifacts are the minimum contract for every canonical module.
REQUIRED_ARTIFACTS=('readme','notebook','tests','app')

def path_for(n:int)->Path|None:
    if n in CANONICAL: return ROOT/CANONICAL[n]
    matches=sorted(ROOT.glob(f'{n:02d}-*'))
    # Prefer the canonical-looking course directory over deprecated duplicates.
    matches=[p for p in matches if p.name not in {'06-rag-first-principles'}] or matches
    return matches[0] if matches else None

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
    structural_missing=[k for k in REQUIRED_ARTIFACTS if not art[k]]
    content_gaps=[k for k,v in ev.items() if not v]+['notebook:'+k for k,v in ne.items() if not v]
    status='COMPLETE' if not structural_missing else 'STRUCTURAL-GAP'
    return {'module':n,'status':status,'score':sum(ev.values())+sum(ne.values())+sum(art.values()),'missing':structural_missing,'content_gaps':content_gaps,'path':str(p.relative_to(ROOT))}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--strict',action='store_true'); a=ap.parse_args()
    results=[score(i) for i in range(1,44)]; complete=sum(x['status']=='COMPLETE' for x in results); content_ready=sum(not x.get('content_gaps') for x in results)
    print('Agentic AI + RAG Course — canonical 43-module QA')
    print('='*72)
    for x in results:
        print(f"M{x['module']:02d}: {x['status']:<14} score={x['score']:02d} path={x.get('path','-')}")
        if x['missing']: print('  structural gaps:',', '.join(x['missing']))
        if x.get('content_gaps'): print('  content backlog:',', '.join(x['content_gaps'][:8]))
    print('='*72)
    print(f'Structurally complete: {complete}/43')
    print(f'Content-template complete: {content_ready}/43')
    print('Strict mode gates structural artifacts only; pedagogical content gaps remain visible as an upgrade backlog.')
    return 0 if (complete==43 or not a.strict) else 1

if __name__=='__main__': raise SystemExit(main())
