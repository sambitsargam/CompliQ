# CompliQ

CompliQ is an AI-powered compliance copilot for small and medium businesses (SMEs). It helps teams ingest policies and contracts, detect gaps, prioritize risks, and produce a remediation action plan with an audit-ready report.

This repository contains a complete full-stack project:

- A **FastAPI backend** with document ingestion, analysis workflows, risk scoring, task generation, and report export.
- A **Next.js frontend** with a landing page and product dashboard.
- A **Neuro-SAN agent layer** for multi-agent orchestration (parser, mapper, gap detector, scorer, planner).

## 1. Product Vision

SMEs often fail compliance readiness because policies are scattered, controls are vague, and audit evidence is not centrally tracked. CompliQ centralizes this workflow in one platform:

1. Upload policy artifacts and operational documents.
2. Analyze controls and obligations.
3. Identify high/medium/low severity gaps.
4. Generate clear remediation tasks with owners and deadlines.
5. Export an audit summary that leadership can review.

## 2. Core Outcomes

CompliQ is designed to produce measurable outputs that are easy to score in a hackathon and practical in real use:

- **Compliance Coverage %**
- **Risk Score (0-100)**
- **Top Findings with Evidence**
- **Prioritized Action Plan**
- **Report Artifact Path / Download**

## 3. Repository Layout

```text
CompliQ/
├── backend/                    # FastAPI service + persistence layer
│   ├── app/
│   │   ├── api/               # HTTP routes
│   │   ├── core/              # settings and DB
│   │   ├── models/            # SQLModel entities
│   │   ├── schemas/           # API request/response contracts
│   │   ├── services/          # ingestion, analysis, report logic
│   │   └── main.py            # app entry point
│   ├── tests/
│   └── requirements.txt
├── frontend/                   # Next.js UI (landing + dashboard)
├── agents/                     # Neuro-SAN registries and coded tools
├── docs/                       # detailed architecture and build docs
├── .env.example
└── .gitignore
```

## 4. Environment Setup

Create local environment variables:

```bash
cp .env.example .env
```

Required values:

- `OPENAI_API_KEY` for LLM-backed analysis paths.
- `DATABASE_URL` defaults to SQLite and works out of the box.

## 5. Run Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend base URL: `http://localhost:8000`

Key routes:

- `GET /health`
- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`
- `POST /api/v1/analysis/run`
- `GET /api/v1/analysis/{analysis_id}`
- `GET /api/v1/tasks`
- `GET /api/v1/reports/{analysis_id}`

## 6. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:3000`

## 7. Neuro-SAN Integration Notes

CompliQ is structured to support a Neuro-SAN multi-agent workflow:

- `ComplianceFrontman`
- `DocParserAgent`
- `RuleMapperAgent`
- `GapDetectorAgent`
- `RiskScorerAgent`
- `ActionPlannerAgent`

The backend includes deterministic analysis logic as a reliable fallback path for local development and demo stability.

## 8. Documentation

Detailed docs are in `docs/`:

- `docs/requirements.md` — functional/non-functional requirements
- `docs/architecture.md` — system architecture and data flow
- `docs/backend-design.md` — backend modules and API contracts
- `docs/development-plan.md` — 12-step implementation plan

## 9. Security and Repository Hygiene

- `.env` is ignored by `.gitignore`
- `.env.example` is versioned and safe to commit
- Local files and generated reports are excluded from Git

## 10. Current Status

- Backend foundation: in progress
- Frontend landing/dashboard: in progress
- Neuro-SAN orchestration wiring: in progress
- End-to-end demo script: planned in later steps
