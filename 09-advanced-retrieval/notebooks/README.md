# Google Colab Notebook Guide

Open `module_09_advanced_retrieval.ipynb` in Google Colab. The notebook is intentionally self-contained so the core retrieval exercises run without API keys or cloud services.

## Learning sequence
1. Run lexical retrieval.
2. Change queries and inspect ranking.
3. Run dense retrieval.
4. Compare lexical/dense failure modes.
5. Combine rankings with RRF.
6. Add labeled evaluation.
7. Implement authorization filtering.
8. Add reranking.
9. Inject retrieval failures.
10. Complete the gold challenge.

## Optional extension
After completing the framework-free notebook, replace the deterministic embedding function with a real embedding model and compare results on the same labeled dataset. Record model/version, dimensions, latency, cost and Recall@K.

## Submission artifact
Create a results table with:
- configuration;
- query class;
- Recall@1/5/10;
- MRR;
- p50/p95 latency;
- candidate count;
- downstream token count;
- failure count;
- security findings;
- final architecture decision.
