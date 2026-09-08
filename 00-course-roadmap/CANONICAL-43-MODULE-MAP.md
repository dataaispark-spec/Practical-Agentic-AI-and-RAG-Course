# Canonical 43-Module Course Map

**Authoritative branch:** `main`  
**Last audited:** 2026-09-09

The numbered directory below is the source of truth for each module. Historical directories retained for compatibility are explicitly non-canonical.

| # | Canonical directory | Primary focus |
|---:|---|---|
| 01 | `01-ai-systems-thinking` | AI systems thinking & architecture decisions |
| 02 | `02-python-ai-engineering` | Python AI engineering / async reliability |
| 03 | `03-fastapi-testing` | FastAPI contracts, streaming, testing |
| 04 | `04-llm-application-foundations` | LLM application foundations |
| 05 | `05-prompting-evaluation` | prompting + evaluation |
| 06 | `06-rag-from-first-principles` | first-principles RAG |
| 07 | `07-embeddings-vector-db` | embeddings + vector databases |
| 08 | `08-document-intelligence-pii` | document intelligence + PII |
| 09 | `09-advanced-retrieval` | hybrid retrieval + reranking |
| 10 | `10-rag-optimization` | optimization, caching, versioning |
| 11 | `11-rag-evaluation` | RAG evaluation + regression |
| 12 | `12-rag-debugging` | RAG debugging + causal investigation |
| 13 | `13-tool-calling-api-agents` | tool calling + API agents |
| 14 | `14-raw-agent-loop` | bounded agent loop |
| 15 | `15-memory` | memory engineering |
| 16 | `16-langgraph-stateful-workflows` | stateful workflows |
| 17 | `17-planning-human-in-the-loop` | planning + human approval |
| 18 | `18-agent-security` | agent security |
| 19 | `19-multi-agent-reality-check` | single vs multi-agent decision science |
| 20 | `20-multi-agent-architectures` | supervisor/worker + multi-agent architectures |
| 21 | `21-coordination-fault-tolerance` | distributed coordination + fault tolerance |
| 22 | `22-multi-agent-debugging` | multi-agent debugging |
| 23 | `23-mcp-fundamentals` | MCP client fundamentals |
| 24 | `24-mcp-server-enterprise` | enterprise MCP server |
| 25 | `25-observability` | AI observability |
| 26 | `26-production-evaluation` | production evaluation + A/B/regression |
| 27 | `27-cost-engineering` | cost-aware routing |
| 28 | `28-responsible-ai-governance` | responsible AI + governance |
| 29 | `29-deployment-cicd` | deployment + CI/CD |
| 30 | `30-enterprise-agentic-rag-capstone` | first integrated enterprise capstone |
| 31 | `31-knowledge-engineering-graph-rag` | knowledge engineering + GraphRAG |
| 32 | `32-graph-engineering-temporal-knowledge` | graph engineering + temporal knowledge |
| 33 | `33-agentic-knowledge-graph-construction` | agentic KG construction |
| 34 | `34-graph-vector-hybrid-retrieval` | graph + vector hybrid retrieval |
| 35 | `35-compounding-knowledge-llm-wiki` | compounding knowledge / LLM wiki |
| 36 | `36-loop-engineering` | production agent loop engineering |
| 37 | `37-harness-engineering` | agent harness engineering |
| 38 | `38-long-running-autonomous-agents` | durable long-running autonomy |
| 39 | `39-skills-memory-continual-harnesses` | skills, memory + continual harnesses |
| 40 | `40-environments-verifiers-agentic-rl` | environments, verifiers + agentic RL |
| 41 | `41-recursive-self-improving-agents` | recursive/self-improving agents |
| 42 | `42-computer-use-always-on-ai-teammates` | computer use + always-on teammates |
| 43 | `43-frontier-graph-rag-agentic-capstone` | frontier Graph-RAG agentic capstone |

## Compatibility aliases

The former frontier directories `31-loop-engineering` through `38-frontier-agentic-rag-capstone` are retained only as historical compatibility copies. They must not be treated as authoritative implementations for canonical numbering.

The former `06-rag-first-principles` and `30-capstone` paths are also legacy aliases. Canonical references, CI, notebooks and learner links must use the directories in the table above.

## Canonical artifact contract

Every canonical module must expose:

- `README.md` with module identity, mission/theory, learning outcomes or mastery gate, architecture/trade-offs, labs/exercises and security/failure guidance;
- `notebooks/` with at least one executable Colab notebook whose title/metadata uses the canonical module number;
- `app/` as the implementation boundary (direct code or an explicit lab-boundary adapter/documentation when the executable reference lives under `labs/`);
- `tests/` with meaningful assertions and failure-path coverage;
- measurable outcomes and a mastery gate;
- explicit dependency linkage to adjacent modules and AegisAI.

## Notebook learning contract

Every canonical notebook should demonstrate:

`Predict → Build → Try → Break → Debug → Measure → Improve → Defend`

Equivalent section names are acceptable, but the behavior must be present rather than merely asserted.

## Certification

Canonical structure, module tests and notebook runtime must all pass before the course is considered QA-certified. Manual semantic review remains required for major curriculum changes.
