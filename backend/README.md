# CompliQ Backend

The backend powers document ingestion, compliance analysis orchestration, persistence, and report generation.

## 1. Responsibilities

1. Receive document uploads.
2. Persist metadata and extracted text.
3. Run compliance analysis (Neuro-SAN first, deterministic fallback).
4. Persist findings, tasks, and report metadata.
5. Return API contracts for frontend/dashboard consumption.

## 2. Stack

- FastAPI
- SQLModel + SQLite (default)
- Optional Neuro-SAN orchestration layer

## 3. Local Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 4. Runtime Paths

- Uploads: `backend/storage/uploads`
- Reports: `backend/storage/reports`
- DB file (default): `backend/compliq.db`

## 5. API Reference

### Health

- `GET /health`
- `GET /api/v1/health`

### Documents

- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`

### Analysis

- `POST /api/v1/analysis/run`
- `GET /api/v1/analysis/{analysis_id}`

### Tasks

- `GET /api/v1/tasks`

### Reports

- `GET /api/v1/reports/{analysis_id}`
- `GET /api/v1/reports/{analysis_id}/content`

## 6. Analysis Strategy

The backend uses this decision order:

1. Try Neuro-SAN structured output if enabled.
2. If Neuro-SAN call fails, fallback to deterministic rules.

This ensures demo reliability while preserving agentic architecture.

## 7. Test/Validation

Quick sanity check:

```bash
python -m compileall app
```

For unit tests, install dev dependencies and run pytest over `backend/tests`.
