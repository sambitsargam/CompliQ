# CompliQ Requirements Specification

## 1. Problem Statement

SMEs need a lightweight, affordable way to evaluate policy readiness and identify compliance gaps without a full legal ops stack.

## 2. Functional Requirements

### FR-1 Document Ingestion

- Users can upload text-based policy artifacts (for MVP: txt/md/doc-like text streams).
- System stores metadata, raw text, and preview snippet.

### FR-2 Compliance Analysis Run

- User selects one or more uploaded documents.
- System triggers an analysis run using selected framework tag (default: `SME-BASELINE`).
- System returns coverage, risk score, findings, and tasks.

### FR-3 Findings Generation

Each finding includes:

- Title
- Severity (`high`, `medium`, `low`)
- Evidence summary
- Recommendation

### FR-4 Action Plan Generation

Each task includes:

- Task title
- Owner
- Priority
- Due-in days
- Status

### FR-5 Report Export

- A report artifact is generated for each analysis run.
- Report includes summary, findings, and action plan.

### FR-6 Dashboard Read APIs

- Fetch document list.
- Fetch analysis details.
- Fetch task list.
- Fetch report reference.

## 3. Non-Functional Requirements

### NFR-1 Fast Local Setup

- Must run without Docker.
- SQLite default required for hackathon speed.

### NFR-2 Explainability

- Findings must include evidence and recommendation text.

### NFR-3 Reliability

- Analysis endpoint should return deterministic output for same input in fallback mode.

### NFR-4 Security Hygiene

- No API keys in source files.
- `.env` must be excluded from git history.

## 4. Tech Requirements

- Backend: FastAPI + SQLModel
- Frontend: Next.js + Tailwind
- Agent Orchestration: Neuro-SAN
- LLM: OpenAI key loaded from `.env`

## 5. MVP Scope

Included in MVP:

- Upload → Analyze → Findings/Tasks → Report flow
- Landing page + dashboard shell
- REST API and DB persistence

Out of scope for MVP:

- Full auth and roles
- Multi-tenant organization controls
- Deep legal citation engine
