"""End-to-end structural and practice-alignment QA for the canonical 43-module course."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from module_objective_map import OBJECTIVES

ROOT=Path(__file__).resolve().parents[1]
CANONICAL={n:f'{n:02d}-' for n in range(1,44)}
CANONICAL.update({6:'06-rag-from-first-principles',30:'30-enterprise-agentic-rag-capstone',31:'31-knowledge-engineering-graph-rag',32:'32-graph-engineering-temporal-knowledge',33:'33-agentic-knowledge-graph-construction',34:'34-graph-vector-hybrid-retrieval',35:'35-compounding-knowledge-llm-wiki',36:'36-loop-engineering',37:'37-harness-engineering',38:'38-long-running-autonomous-agents',39:'39-skills-memory-continual-harnesses',40:'40-environments-verifiers-agentic-rl',41:'41-recursive-self-improving-agents',42:'42-computer-use-always-on-ai-teammates',43:'43-frontier-graph-rag-agentic-capstone'})
EXPECTED={1:'AI Systems Thinking',2:'Python',3:'FastAPI',4:'LLM Application Foundations',5:'Prompting',6:'RAG',7:'Embeddings',8:'Document Intelligence',9:'Advanced Retrieval',10:'RAG Optimization',11:'RAG Evaluation',12:'RAG Debugging',13:'Tool Calling',14:'Raw Agent Loop',15:'Memory',16:'Stateful',17:'Planning',18:'Agent Security',19:'Multi-Agent Reality Check',20:'Multi-Agent Architectures',21:'Coordination',22:'Multi-Agent Debugging',23:'MCP Fundamentals',24:'MCP',25:'Observability',26:'Production Evaluation',27:'Cost Engineering',28:'Responsible AI',29:'Deployment',30:'Enterprise Agentic RAG',31:'Knowledge Engineering',32:'Graph Engineering',33:'Agentic Knowledge Graph',34:'Graph + Vector Hybrid',35:'Compounding Knowledge',36:'Loop Engineering',37:'Harness Engineering',38:'Long-Running',39:'Skills, Memory',40:'Environments',41:'Recursive',42:'Computer Use',43:'Frontier Graph-RAG'}

def path_for(n):
    t=CANONICAL[n]
    if t.endswith('-'):
        ms=sorted(p for p in ROOT.glob(t+'*') if p.is_dir())
        return ms[0] if ms else None
    d=ROOT/t
    return d if d.is_dir() else None

def read(p):
    try:return p.read_text(encoding='utf-8',errors='ignore')
    except OSError:return ''

def notebook_data(d):
    out=[]; nd=d/'notebooks'
    if not nd.is_dir(): return out
    for p in sorted(nd.glob('*.ipynb')):
        try:
            obj=json.loads(p.read_text(encoding='utf-8'))
            text='\n'.join(''.join(c.get('source',[])) if isinstance(c.get('source',[]),list) else str(c.get('source','')) for c in obj.get('cells',[]))
            out.append((p,text,obj))
        except Exception as e: out.append((p,'',None))
    return out

def phrase_present(term,text):
    norm=re.sub(r'[^a-z0-9]+',' ',text.lower())
    words=[w for w in re.sub(r'[^a-z0-9]+',' ',term.lower()).split() if len(w)>2]
    if not words:return True
    return sum(w in norm for w in words)>=max(1,(len(words)+1)//2)

def title_ok(n,r):
    m=re.search(r'^#\s+Module\s+(\d+)\s+[—-]\s+(.+)$',r,re.M)
    return bool(m and int(m.group(1))==n and EXPECTED[n].lower() in m.group(2).lower())

def score(n):
    d=path_for(n)
    if d is None:return {'module':n,'status':'MISSING','path':'','issues':['module directory missing']}
    r=read(d/'README.md'); data=notebook_data(d); nb='\n'.join(x[1] for x in data)
    # The course-wide deep-practice pack is a companion specification; local artifacts still must exist.
    pack=read(ROOT/'00-course-roadmap'/'MODULE-DEEP-PRACTICE-IMPLEMENTATION-PACK.md')
    combined=(r+'\n'+nb+'\n'+pack).lower(); issues=[]
    if not (d/'README.md').is_file():issues.append('README.md missing')
    if not data:issues.append('executable notebook missing')
    if any(obj is None for _,_,obj in data):issues.append('invalid notebook JSON')
    if not (d/'app').is_dir():issues.append('app boundary missing')
    if not list(d.rglob('test_*.py')):issues.append('tests missing')
    if not title_ok(n,r):issues.append('README module identity/title mismatch')
    terms=OBJECTIVES[n]; hits=sum(phrase_present(t,combined) for t in terms)
    if hits < max(3,min(5,len(terms))):issues.append(f'objective coverage {hits}/{len(terms)} below gate')
    # Marker evidence may live in the notebook or in the explicit module practice specification.
    aliases={'BUILD':('build','implement','construct','baseline'),'TRY':('try','experiment','ablation','exercise'),'BREAK':('break','failure','fault','debug','adversarial','inject','chaos'),'MEASURE':('measure','metric','evaluation','latency','cost','benchmark','recall','mrr','success rate')}
    for marker,words in aliases.items():
        if not any(w in nb.lower() for w in words) and not any(w in r.lower() for w in words):issues.append(f'practice evidence missing: {marker}')
    if not re.search(r'(?i)(learning outcomes|learning goals|objectives|mastery gate)',r):issues.append('README lacks explicit learning-outcome/mastery section')
    return {'module':n,'status':'PASS' if not issues else 'REVIEW','path':str(d.relative_to(ROOT)),'objective_hits':hits,'objective_total':len(terms),'issues':issues}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--strict',action='store_true');args=ap.parse_args();results=[score(n) for n in range(1,44)]
    for x in results:
        print(f"M{x['module']:02d}: {x['status']:<6} {x['path']}")
        for i in x.get('issues',[]):print('  -',i)
    passed=sum(x['status']=='PASS' for x in results);print(f'End-to-end alignment QA: {passed}/43 pass')
    if args.strict and passed!=43:return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
