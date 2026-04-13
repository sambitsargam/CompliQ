# CompliQ Runbook

This runbook is for hackathon demo day and local validation.

## 1. Prerequisites

Required tools:
- Python 3.13+
- Node.js 18+
- npm

Required file:
- `.env` in repository root (copied from `.env.example`)

## 2. Environment Setup

From repo root:

```bash
cp .env.example .env
```

Set at least:

```env
OPENAI_API_KEY=your_openai_api_key_here
USE_NEURO_SAN=true
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Optional for Neuro-SAN worker behavior:

```env
NEURO_SAN_MP_START_METHOD=spawn
```

Optional but recommended for backend started from `backend/`:

```env
AGENT_MANIFEST_FILE=../agents/registries/manifest.hocon
AGENT_TOOL_PATH=../agents/coded_tools
```

## 3. Start Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verification:
- open `http://localhost:8000/health`
- expect `{"status":"ok","service":"CompliQ API"}`

## 4. Start Frontend

In new terminal:

```bash
cd frontend
npm install
npm run dev
```

Verification:
- open `http://localhost:3000`
- navigate to `/dashboard`

## 5. Standard Smoke Test (2-3 minutes)

1. Open dashboard.
2. Confirm health card shows `Healthy`.
3. Upload a sample text policy file.
4. Select uploaded document.
5. Click `Run Compliance Analysis`.
6. Verify output appears:
- coverage
- risk score
- findings
- tasks
- report content

Pass criteria:
- no unhandled frontend error
- analysis details visible
- report content endpoint resolves

## 6. Demo Script (Judge Walkthrough)

1. Explain problem: SMEs struggle with fragmented compliance docs.
2. Show landing page value proposition.
3. Open dashboard and show health + ready state.
4. Upload one weak sample policy text.
5. Run analysis and narrate scoring.
6. Expand findings with evidence/recommendations.
7. Show generated remediation tasks.
8. Show report content as exportable artifact.
9. Mention Neuro-SAN strict mode + explicit error visibility.

## 7. Contingency Playbook

### Case A: Neuro-SAN fails or times out

Action:
- keep `USE_NEURO_SAN=true` to show strict agentic behavior
- if needed for backup demo, set `USE_NEURO_SAN=false` to use local deterministic mode
- rerun analysis and explain mode switch clearly

Message to judges:
- architecture supports strict agentic execution with a transparent backup mode

### Case B: Backend unreachable from frontend

Checks:
1. backend terminal still running
2. backend port is `8000`
3. `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`

### Case C: No documents found on analysis

Checks:
- ensure at least one document is selected
- confirm document list call returns IDs

### Case D: Report metadata exists but content is missing

Checks:
- verify `storage/reports` write permissions
- rerun analysis to regenerate report

## 8. Quick Health Commands

Backend health:

```bash
curl -s http://localhost:8000/health
```

Documents list:

```bash
curl -s http://localhost:8000/api/v1/documents
```

Tasks list:

```bash
curl -s http://localhost:8000/api/v1/tasks
```

## 9. Shutdown Procedure

- Stop frontend: `Ctrl+C` in frontend terminal
- Stop backend: `Ctrl+C` in backend terminal
- Deactivate virtual env if active: `deactivate`

## 10. Post-Demo Checklist

- confirm no secrets were committed
- ensure latest docs and code are pushed
- capture a short demo recording while environment is still warm
- tag commit used for submission demo
