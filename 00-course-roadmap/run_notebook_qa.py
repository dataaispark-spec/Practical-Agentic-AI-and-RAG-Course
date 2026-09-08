from __future__ import annotations
import argparse, os, sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
CANONICAL={31:'31-knowledge-engineering-graph-rag',32:'32-graph-engineering-temporal-knowledge',33:'33-agentic-knowledge-graph-construction',34:'34-graph-vector-hybrid-retrieval',35:'35-compounding-knowledge-llm-wiki',36:'31-loop-engineering',37:'32-harness-engineering',38:'33-long-running-autonomous-agents',39:'34-skills-memory-continual-harnesses',40:'35-environments-verifiers-agentic-rl',41:'36-recursive-self-improving-agents',42:'37-computer-use-always-on-ai-teammates',43:'38-frontier-agentic-rag-capstone'}

def notebooks(modules:list[int]):
    for n in modules:
        d=ROOT/CANONICAL[n] if n in CANONICAL else next(iter(sorted(ROOT.glob(f'{n:02d}-*'))),None)
        if d and (d/'notebooks').exists():
            for p in sorted((d/'notebooks').glob('*.ipynb')): yield n,p

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--modules',default='4-43'); ap.add_argument('--timeout',type=int,default=300); ap.add_argument('--continue-on-error',action='store_true'); args=ap.parse_args()
    start,end=map(int,args.modules.split('-')); os.environ.setdefault('MOCK_LLM','true'); os.environ.setdefault('OPENAI_API_KEY',''); os.environ.setdefault('ANTHROPIC_API_KEY','')
    failures=[]; total=0
    for n,p in notebooks(range(start,end+1)):
        total+=1; print(f'EXECUTE M{n:02d}: {p.relative_to(ROOT)}')
        try:
            nb=nbformat.read(p,as_version=4)
            module_root=p.parent.parent
            existing=os.environ.get('PYTHONPATH','')
            os.environ['PYTHONPATH']=str(module_root)+(os.pathsep+existing if existing else '')
            client=NotebookClient(nb,timeout=args.timeout,kernel_name='python3',resources={'metadata':{'path':str(p.parent)}})
            client.execute()
            print(f'PASS M{n:02d}: {p.name}')
        except Exception as exc:
            failures.append((n,p,str(exc))); print(f'FAIL M{n:02d}: {p.name}: {exc}')
            if not args.continue_on_error: break
    print(f'Notebook QA: {total-len(failures)}/{total} passed')
    if failures:
        print('Failures:'); [print(f'- M{n:02d} {p}: {e}') for n,p,e in failures]; return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
