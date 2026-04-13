# CompliQ 12-Step Development Plan

This plan is designed for hackathon execution with incremental delivery and push-after-each-step discipline.

## Step 1: Define Score-Driven Product Positioning

Objective:
- map app outputs to judging criteria (innovation, implementation quality, usefulness, clarity)

Deliverables:
- one-sentence product statement
- clear target user (SMEs)
- measurable outputs (coverage, risk, findings, tasks, report)

Done criteria:
- team agrees on single MVP narrative

## Step 2: Freeze MVP Scope and Constraints

Objective:
- avoid scope drift and preserve demo reliability

Deliverables:
- must-have feature list
- out-of-scope list
- stack constraints (no Docker, local run)

Done criteria:
- frozen requirement doc in `docs/requirements.md`

## Step 3: Create Repository Skeleton

Objective:
- establish clean project structure for backend/frontend/agents/docs

Deliverables:
- directory scaffold
- base readme and placeholder docs

Done criteria:
- monorepo structure ready for parallel implementation

## Step 4: Environment and Git Hygiene

Objective:
- ensure secure and reproducible local development

Deliverables:
- `.gitignore`
- `.env.example`
- root quick-start instructions

Done criteria:
- `.env` is ignored
- no secret appears in git status

## Step 5: Backend Foundation

Objective:
- boot FastAPI and persistence baseline

Deliverables:
- settings loader
- DB session + initialization
- health routes
- initial tests

Done criteria:
- API server boots and health returns `ok`

## Step 6: Document Ingestion

Objective:
- support upload and storage of source artifacts

Deliverables:
- upload endpoint
- file persistence service
- document metadata model
- list documents endpoint

Done criteria:
- uploaded file appears in dashboard-readable API response

## Step 7: Analysis Workflow

Objective:
- produce core compliance outputs and persist run artifacts

Deliverables:
- run-analysis endpoint
- scoring + finding + task contract
- persistence of run/finding/task/report entities

Done criteria:
- API returns analysis summary with counts and report path

## Step 8: Neuro-SAN Integration Layer

Objective:
- add agentic orchestration path without breaking reliability

Deliverables:
- Neuro-SAN registry definitions
- coded tools
- backend adapter
- strict error handling logic

Done criteria:
- backend attempts Neuro-SAN and returns explicit failures in strict mode

## Step 9: Landing Page and Dashboard UI

Objective:
- provide polished judge-friendly presentation and workspace

Deliverables:
- branded landing page
- dashboard shell with core panels
- reusable UI components

Done criteria:
- navigation and layout stable on desktop and mobile

## Step 10: Frontend-Backend Integration

Objective:
- complete full end-to-end user flow

Deliverables:
- upload integration
- analysis trigger integration
- findings/tasks/report rendering
- error messaging

Done criteria:
- full flow works through UI only

## Step 11: Validation and Demo Hardening

Objective:
- reduce live demo failure risk

Deliverables:
- compile/test checks
- smoke run procedure
- troubleshooting notes

Done criteria:
- repeatable local run in under 15 minutes

## Step 12: Submission Packaging

Objective:
- present project clearly for scoring and review

Deliverables:
- architecture and design docs
- runbook and checklist
- 1-2 page summary alignment
- demo script

Done criteria:
- reviewer can understand and run project from docs only

## Working Method for Each Step

For each step:
1. implement scoped changes
2. validate locally
3. update docs
4. commit with clear message
5. push to remote

This keeps progress auditable and avoids last-minute integration debt.

## Risk Controls Across Steps

- keep API contracts stable once frontend integration starts
- avoid introducing non-essential dependencies late
- keep strict timeout and clear error path intact until end of event
- keep docs updated in same commit as code changes
