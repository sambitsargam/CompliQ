# CompliQ

CompliQ is an AI-powered compliance copilot for small and medium businesses (SMEs).

It helps teams convert scattered policy text into a clear compliance posture:
- What is covered
- What is missing
- What is high risk
- What to fix first
- What report to show during review or audit

The project is designed for hackathon delivery with strong judging alignment: practical business value, clear agentic architecture, explainable outputs, and an end-to-end live demo.

## Product Snapshot

CompliQ currently supports this complete workflow:
1. Upload policy or process documents.
2. Select one or more documents for a run.
3. Trigger compliance analysis.
4. Receive coverage percentage and risk score.
5. Review findings with evidence and recommendations.
6. Review remediation tasks with priorities and due windows.
7. Open generated report content directly in the dashboard.

## Why This Matters

SMEs often struggle with compliance because:
- Policies exist but are fragmented.
- Ownership is unclear.
- Review cadence is not defined.
- Incident and retention controls are incomplete.
- Teams lack a lightweight way to prioritize remediation.

CompliQ addresses this by combining deterministic checks (stable and fast) with an agentic Neuro-SAN path (advanced and extensible).

## Tech Stack

- Backend: FastAPI + SQLModel + SQLite
- Frontend: Next.js App Router + TypeScript + Tailwind CSS
- Agent Layer: Neuro-SAN (frontman + specialist agents + coded tools)
- LLM Key Source: `.env` (`OPENAI_API_KEY`)

## Repository Structure

```text
CompliQ/
├── agents/                     # Neuro-SAN registries and coded tools
│   ├── registries/
│   └── coded_tools/
├── backend/                    # FastAPI app
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   └── requirements.txt
├── frontend/                   # Next.js landing page + dashboard
│   ├── app/
│   ├── components/
│   └── lib/
├── docs/                       # Detailed technical and submission docs
├── .env.example
└── .gitignore
```

## Quick Start

### 1. Clone and enter repository

```bash
git clone https://github.com/sambitsargam/CompliQ.git
cd CompliQ
```

### 2. Configure environment

```bash
cp .env.example .env
```

Update `.env` values as needed:
- `OPENAI_API_KEY`
- `USE_NEURO_SAN`
- `NEXT_PUBLIC_API_BASE_URL`

### 3. Run backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend should be available at `http://localhost:8000`.

### 4. Run frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend should be available at `http://localhost:3000`.

### 5. Demo flow

1. Open `/dashboard`.
2. Upload a sample policy text file.
3. Select the uploaded document.
4. Run analysis.
5. Review findings/tasks/report content.

## Runtime Behavior: Neuro-SAN Modes

CompliQ analysis follows this logic:
1. If `USE_NEURO_SAN=true`, backend requires Neuro-SAN orchestration.
2. If Neuro-SAN succeeds and returns valid JSON, that result is used.
3. If Neuro-SAN fails or output is invalid, backend returns explicit `502` error.
4. If `USE_NEURO_SAN=false`, backend uses optional deterministic local mode.
5. Neuro-SAN worker process defaults to multiprocessing `spawn` mode (`NEURO_SAN_MP_START_METHOD=spawn`).

This design gives both:
- agentic architecture for innovation scoring
- strict Neuro-SAN execution when enabled

## API Overview

Core endpoints:
- `GET /health`
- `GET /api/v1/health`
- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`
- `GET /api/v1/frameworks`
- `GET /api/v1/neuro-san/status`
- `POST /api/v1/analysis/run`
- `GET /api/v1/analysis`
- `GET /api/v1/analysis/{analysis_id}`
- `GET /api/v1/tasks`
- `PATCH /api/v1/tasks/{task_id}`
- `GET /api/v1/reports/{analysis_id}`
- `GET /api/v1/reports/{analysis_id}/content`
- `GET /api/v1/reports/{analysis_id}/download`

Full contract details are in `docs/api-reference.md`.

## Documentation Map

- `docs/requirements.md`: product and system requirements
- `docs/architecture.md`: system architecture and data flow
- `docs/backend-design.md`: backend modules, models, and service behavior
- `docs/frontend-design.md`: UX and client architecture
- `docs/agent-design.md`: Neuro-SAN network and tooling
- `docs/development-plan.md`: detailed 12-step build plan
- `docs/runbook.md`: day-of-demo operational guide
- `docs/submission-checklist.md`: hackathon evidence checklist
- `docs/roadmap.md`: post-hackathon growth plan

## Security and Repo Hygiene

- `.env` is ignored and never committed.
- `.env.example` is versioned with safe placeholders.
- No secrets should be hardcoded in source files.
- Local runtime artifacts are excluded from Git.

## What Is Production-Ready vs MVP

MVP included now:
- Upload, analyze, findings, tasks, report flow
- Landing page + dashboard
- Persistent data model in SQLite
- Neuro-SAN adapter with strict timeout + explicit error path
- Framework packs (`SME-BASELINE`, `DATA-PRIVACY`, `INCIDENT-READY`)
- Control scorecard and analysis run history
- Startup-style task manager with status workflow (`open`, `in_progress`, `done`)

Planned next:
- Authentication and role-based access
- Multi-tenant workspace boundaries
- Deep parser support for PDF/DOCX
- Integrations (ticketing, alerts, exports)

## Contribution Notes

If you continue implementation during the hackathon:
- Keep API contracts stable.
- Add tests for all new endpoints.
- Update docs in `docs/` for every feature change.
- Keep commits small and demo-safe.
