# Canonical 43-Module Course Map

**Authority:** normative source of truth for module identity and canonical paths  
**Branch:** `main`  
**Last audited:** 2026-09-09

All learner-facing links, CI paths, notebook identities and implementation references should use this map. Historical compatibility copies are not additional curriculum modules.

## Core — Modules 01–30

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

## Knowledge engineering & graph — Modules 31–35

| # | Canonical directory | Primary focus |
|---:|---|---|
| 31 | `31-knowledge-engineering-graph-rag` | knowledge engineering + GraphRAG |
| 32 | `32-graph-engineering-temporal-knowledge` | graph engineering + temporal knowledge |
| 33 | `33-agentic-knowledge-graph-construction` | agentic KG construction |
| 34 | `34-graph-vector-hybrid-retrieval` | graph + vector hybrid retrieval |
| 35 | `35-compounding-knowledge-llm-wiki` | compounding knowledge / LLM wiki |

## Frontier agent engineering — Modules 36–43

| # | Canonical directory | Primary focus |
|---:|---|---|
| 36 | `36-loop-engineering` | production agent loop engineering |
| 37 | `37-harness-engineering` | agent harness engineering |
| 38 | `38-long-running-autonomous-agents` | durable long-running autonomy |
| 39 | `39-skills-memory-continual-harnesses` | skills, memory + continual harnesses |
| 40 | `40-environments-verifiers-agentic-rl` | environments, verifiers + agentic RL |
| 41 | `41-recursive-self-improving-agents` | recursive/self-improving agents |
| 42 | `42-computer-use-always-on-ai-teammates` | computer use + always-on teammates |
| 43 | `43-frontier-graph-rag-agentic-capstone` | frontier Graph-RAG agentic capstone |

## Curriculum progression

```text
01–05  Foundations
  ↓
06–12  RAG engineering
  ↓
13–18  Tools / loops / memory / state / planning / security
  ↓
19–24  Multi-agent / MCP
  ↓
25–30  Production engineering + first AegisAI capstone
  ↓
31–35  Knowledge / graph engineering
  ↓
36–43  Frontier loop / harness / durability / continual learning / verifiers / self-improvement / computer use / final capstone
```

## Canonical artifact expectations

Every canonical module should expose, directly or through an explicit companion boundary:

- `README.md` with module identity, theory/mechanism, architecture, exercises, failure/security guidance and mastery expectations;
- at least one executable notebook under `notebooks/` whose filename and metadata use the canonical module number;
- an `app/` implementation boundary or explicit documented lab boundary;
- meaningful tests with failure-path coverage;
- measurable learning outcomes and a mastery gate;
- prerequisite/successor and AegisAI links.

Exact notebook structure is governed by [`COLAB-PRACTICE-NOTEBOOK-STANDARD.md`](./COLAB-PRACTICE-NOTEBOOK-STANDARD.md). Course-wide engineering principles are governed by [`COURSE-ENGINEERING-STANDARDS.md`](./COURSE-ENGINEERING-STANDARDS.md).

## Legacy path policy

The former duplicate frontier paths `31-loop-engineering` through `38-frontier-agentic-rag-capstone`, plus the obsolete `30-capstone` alias, have been removed from `main`. They are historical implementation paths only and must not be recreated.

The canonical course now has **one physical directory per module 01–43**. If historical material is needed later, recover it from Git history and merge only the specific content that improves the canonical module.

## Identity rule

A canonical module's README title, notebook filename/metadata, tests and implementation references must agree on its canonical number and name. Historical numbering inside dated migration records is acceptable only when clearly labeled as historical.

## Certification reminder

Canonical structure is necessary but not sufficient for course quality. Structural QA, module tests, clean-kernel notebook runtime and aggregate CI must be complemented by manual semantic review before the course is called certified.
