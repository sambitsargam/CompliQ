# CompliQ

CompliQ is an AI-powered compliance copilot for SMEs. It ingests business documents, identifies compliance gaps, scores risk, and generates action plans with audit-ready summaries.

## Monorepo Structure

- `backend/` FastAPI API + SQLite persistence
- `frontend/` Next.js landing page + dashboard UI
- `agents/` Neuro-SAN agent network for compliance analysis
- `docs/` architecture and development notes

## Quick Start

### 1) Environment

```bash
cp .env.example .env
# Set OPENAI_API_KEY in .env
```

### 2) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

Backend runs at `http://localhost:8000`.

### 3) Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`.

## MVP Features

- Document upload and parsing
- Compliance analysis job execution
- Risk scoring and prioritized findings
- Action task generation
- Report export endpoint
- Landing page + dashboard UI

## Notes

- Default DB is SQLite for fastest local setup.
- Neuro-SAN usage is enabled by default (`USE_NEURO_SAN=true`) and falls back safely if unavailable.
