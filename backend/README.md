# CompliQ Backend

The backend is the execution core of CompliQ. It handles document ingestion, analysis orchestration, persistence, and report generation.

## Responsibilities

The backend service is responsible for:
1. Accepting document uploads.
2. Persisting raw text and metadata.
3. Running compliance analysis (Neuro-SAN first, deterministic fallback).
4. Persisting findings, tasks, and report references.
5. Serving dashboard-ready APIs.

## Stack

- FastAPI for HTTP APIs
- SQLModel for ORM/data model
- SQLite as default database for hackathon speed
- Optional Neuro-SAN integration for agentic orchestration

## Directory Structure

```text
backend/
├── app/
│   ├── api/                   # FastAPI routers
│   ├── core/                  # settings and DB session
│   ├── models/                # SQLModel entities
│   ├── schemas/               # request/response contracts
│   ├── services/              # upload, analysis, report services
│   └── main.py                # FastAPI app bootstrap
├── tests/
└── requirements.txt
```

## Setup

### 1. Create environment and install dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create project env file (from repo root)

```bash
cp ../.env.example ../.env
```

### 3. Run API server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Base URL: `http://localhost:8000`

## Key Configuration

Values are loaded from `.env` via `pydantic-settings`.

- `DATABASE_URL` default: `sqlite:///./compliq.db`
- `USE_NEURO_SAN` default: `true`
- `OPENAI_API_KEY` for agentic LLM path
- `AGENT_MANIFEST_FILE` default expected: `../agents/registries/manifest.hocon`
- `AGENT_TOOL_PATH` default expected: `../agents/coded_tools`
- `CORS_ORIGINS` default: `http://localhost:3000`

## Runtime Paths

By default, when running from `backend/`:
- Uploads: `backend/storage/uploads`
- Reports: `backend/storage/reports`
- SQLite DB: `backend/compliq.db`

## API Surface

### Health
- `GET /health`
- `GET /api/v1/health`

### Document APIs
- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`

### Analysis APIs
- `POST /api/v1/analysis/run`
- `GET /api/v1/analysis/{analysis_id}`

### Task APIs
- `GET /api/v1/tasks`

### Report APIs
- `GET /api/v1/reports/{analysis_id}`
- `GET /api/v1/reports/{analysis_id}/content`

Detailed request/response contracts are documented in `../docs/api-reference.md`.

## Analysis Execution Logic

`run_compliance_analysis(merged_text)` executes with this order:
1. If `USE_NEURO_SAN=true`, attempt `run_neuro_san_analysis`.
2. If agent output is valid, return it.
3. If agent call fails, run deterministic heuristic checks.

Deterministic checks currently evaluate presence/absence of:
- policy ownership language
- review cadence
- incident escalation language
- data retention language
- access control language

Outputs include:
- `coverage_percent`
- `risk_score`
- `summary`
- `findings[]`
- `tasks[]`

## Data Model

Main SQLModel entities:
- `Document`
- `AnalysisRun`
- `Finding`
- `TaskItem`
- `Report`

A single analysis run produces multiple findings and tasks, and one report record.

## Local Validation

### Compile check

```bash
python -m compileall app
```

### Run tests

```bash
pytest -q
```

(If pytest dependencies are missing, install them first.)

## Common Issues

1. `404` on analysis run with selected IDs:
- Verify document IDs exist in `GET /api/v1/documents`.

2. Neuro-SAN not loading:
- Ensure backend is started from `backend/`.
- Ensure `AGENT_MANIFEST_FILE` and `AGENT_TOOL_PATH` paths are valid.
- Confirm `OPENAI_API_KEY` is available in `.env`.

3. Frontend cannot call backend:
- Ensure backend is on port `8000`.
- Confirm `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`.

## Extension Guidance

When adding features:
- Keep API contracts backward compatible.
- Add request/response schema updates in `app/schemas/contracts.py`.
- Persist all new domain entities via SQLModel migrations strategy (for MVP, manual DB reset is acceptable).
- Update docs in `../docs` for every behavior change.
