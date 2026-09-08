from __future__ import annotations
import argparse, os
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[1]

def notebooks(modules: list[int]):
    for n in modules:
        dirs=sorted(ROOT.glob(f'{n:02d}-*'))
        for d in dirs:
            for p in sorted((d/'notebooks').glob('*.ipynb')) if (d/'notebooks').exists() else []:
                yield n,p

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--modules',default='4-38'); ap.add_argument('--timeout',type=int,default=300); ap.add_argument('--continue-on-error',action='store_true'); args=ap.parse_args()
    start,end=map(int,args.modules.split('-')); os.environ.setdefault('MOCK_LLM','true'); os.environ.setdefault('OPENAI_API_KEY',''); os.environ.setdefault('ANTHROPIC_API_KEY','')
    failures=[]; total=0
    for n,p in notebooks(list(range(start,end+1))):
        total+=1; print(f'EXECUTE M{n:02d}: {p.relative_to(ROOT)}')
        try:
            nb=nbformat.read(p,as_version=4)
            NotebookClient(nb,timeout=args.timeout,kernel_name='python3',resources={'metadata':{'path':str(p.parent)}}).execute()
            print(f'PASS M{n:02d}: {p.name}')
        except Exception as exc:
            failures.append((n,p,str(exc))); print(f'FAIL M{n:02d}: {p.name}: {exc}')
            if not args.continue_on_error: break
    print(f'Notebook QA: {total-len(failures)}/{total} passed')
    if failures:
        print('Failures:'); [print(f'- M{n:02d} {p}: {e}') for n,p,e in failures]
        return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
