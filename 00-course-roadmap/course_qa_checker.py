"""Structural + semantic alignment QA for the canonical 43-module course."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from module_objective_map import OBJECTIVES

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = {n: f'{n:02d}-' for n in range(1, 44)}
CANONICAL.update({6:'06-rag-from-first-principles',30:'30-enterprise-agentic-rag-capstone',31:'31-knowledge-engineering-graph-rag',32:'32-graph-engineering-temporal-knowledge',33:'33-agentic-knowledge-graph-construction',34:'34-graph-vector-hybrid-retrieval',35:'35-compounding-knowledge-llm-wiki',36:'36-loop-engineering',37:'37-harness-engineering',38:'38-long-running-autonomous-agents',39:'39-skills-memory-continual-harnesses',40:'40-environments-verifiers-agentic-rl',41:'41-recursive-self-improving-agents',42:'42-computer-use-always-on-ai-teammates',43:'43-frontier-graph-rag-agentic-capstone'})
EXPECTED_TITLES = {1:'AI Systems Thinking',2:'Python for AI Engineering',3:'FastAPI',4:'LLM Application Foundations',5:'Prompting',6:'RAG',7:'Embeddings',8:'Document Intelligence',9:'Advanced Retrieval',10:'RAG Optimization',11:'RAG Evaluation',12:'RAG Debugging',13:'Tool Calling',14:'Raw Agent Loop',15:'Memory',16:'Stateful Agent Workflows',17:'Planning',18:'Agent Security',19:'Multi-Agent Reality Check',20:'Multi-Agent Architectures',21:'Multi-Agent Coordination',22:'Multi-Agent Debugging',23:'MCP Fundamentals',24:'MCP Server',25:'Observability',26:'Production Evaluation',27:'Cost Engineering',28:'Responsible AI',29:'Deployment',30:'Enterprise Agentic RAG',31:'Knowledge Engineering',32:'Graph Engineering',33:'Agentic Knowledge Graph',34:'Graph + Vector Hybrid',35:'Compounding Knowledge',36:'Loop Engineering',37:'Harness Engineering',38:'Long-Running',39:'Skills, Memory',40:'Environments',41:'Recursive',42:'Computer Use',43:'Frontier Graph-RAG'}


def path_for(n:int)->Path|None:
    target = CANONICAL[n]
    if target.endswith('-'):
        matches = sorted(ROOT.glob(f'{target}*'))
        matches = [p for p in matches if p.is_dir() and p.name != '06-rag-first-principles' and p.name != '30-capstone']
        return matches[0] if matches else None
    d = ROOT / target
    return d if d.exists() else None


def read(p:Path)->str:
    try:return p.read_text(encoding='utf-8',errors='ignore')
    except OSError:return ''


def notebook_texts(d:Path)->list[str]:
    out=[]
    nd=d/'notebooks'
    if not nd.exists(): return out
    for p in sorted(nd.glob('*.ipynb')):
        try:
            obj=json.loads(p.read_text(encoding='utf-8'))
            out.append('\n'.join(''.join(c.get('source',[])) if isinstance(c.get('source',[]),list) else str(c.get('source','')) for c in obj.get('cells',[])))
        except Exception: out.append('')
    return out


def title_ok(n:int, r:str)->bool:
    m=re.search(r'^#\s+Module\s+(\d+)\s+—\s+(.+)$',r,re.M)
    return bool(m and int(m.group(1))==n and EXPECTED_TITLES[n].lower() in m.group(2).lower())


def phrase_present(term:str, text:str)->bool:
    norm = re.sub(r'[^a-z0-9]+',' ',text.lower())
    words = [w for w in re.sub(r'[^a-z0-9]+',' ',term.lower()).split() if len(w)>2]
    if not words: return True
    # Require substantial lexical overlap rather than an exact punctuation-sensitive phrase.
    return sum(w in norm for w in words) >= max(1, (len(words)+1)//2)


def score(n:int)->dict:
    d=path_for(n)
    if d is None: return {'module':n,'status':'MISSING','path':'','issues':['module directory missing']}
    r=read(d/'README.md'); nbs=notebook_texts(d); nb='\n'.join(nbs); combined=(r+'\n'+nb).lower()
    issues=[]
    if not (d/'README.md').exists(): issues.append('README.md missing')
    if not nbs: issues.append('notebook missing')
    if not (d/'app').exists(): issues.append('app missing')
    if not list(d.rglob('test_*.py')): issues.append('tests missing')
    if not title_ok(n,r): issues.append('README module identity/title mismatch')
    terms=[x.lower() for x in OBJECTIVES[n]]
    objective_hits=sum(phrase_present(t,combined) for t in terms)
    for t in terms:
        if not phrase_present(t,combined): issues.append(f'objective evidence missing: {t}')
    marker_aliases={
        'BUILD':('build','implement','create','construct'),
        'TRY':('try','experiment','lab','exercise','run'),
        'BREAK':('break','failure','fault','debug','adversarial','inject'),
        'MEASURE':('measure','metric','evaluation','latency','cost','benchmark'),
    }
    for marker, aliases in marker_aliases.items():
        if not any(a in nb.lower() for a in aliases): issues.append(f'notebook marker/equivalent missing: {marker}')
    if r and not re.search(r'(?i)(learning outcomes|learning goals|objectives|mastery gate)',r): issues.append('README lacks explicit learning-outcome/mastery section')
    if nbs and objective_hits < max(2, min(4,len(terms))): issues.append('weak objective-to-artifact coverage')
    return {'module':n,'status':'PASS' if not issues else 'REVIEW','path':str(d.relative_to(ROOT)),'objective_hits':objective_hits,'objective_total':len(terms),'issues':issues}


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--strict',action='store_true'); args=ap.parse_args()
    results=[score(n) for n in range(1,44)]
    for x in results:
        print(f"M{x['module']:02d}: {x['status']:<6} {x['path']}")
        for issue in x.get('issues',[]): print('  -',issue)
    passed=sum(x['status']=='PASS' for x in results)
    print(f'Alignment QA: {passed}/43 pass')
    if args.strict and passed!=43: return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
