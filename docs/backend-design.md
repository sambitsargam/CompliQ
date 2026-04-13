# CompliQ Backend Design

## 1. Design Objectives

The backend is designed to maximize:
- Reliability under hackathon demo conditions
- Clear and stable API contracts for frontend integration
- Easy extension toward richer agentic analysis
- Fast local setup without infrastructure overhead

## 2. Module Boundaries

`app/main.py`
- FastAPI bootstrap
- global startup initialization
- top-level health endpoint
- API router include

`app/core/config.py`
- environment-backed settings
- feature flags (`USE_NEURO_SAN`)
- runtime directory paths

`app/core/database.py`
- SQLModel engine creation
- session factory and dependency injection
- DB initialization helpers

`app/models/entities.py`
- persistent entities for documents, runs, findings, tasks, reports

`app/schemas/contracts.py`
- request and response contract classes
- typed analysis payload shape

`app/services/document_service.py`
- upload handling
- content extraction and safe preview generation

`app/services/agent_service.py`
- analysis orchestration decision
- strict Neuro-SAN mode with optional deterministic local mode

`app/services/neuro_san_adapter.py`
- Neuro-SAN session setup
- response streaming + JSON extraction
- schema adaptation into backend contract

`app/services/report_service.py`
- markdown report content builder
- report file persistence

`app/api/routes.py`
- route handlers
- DB writes/reads
- API response shaping

## 3. Data Model

### Document

Purpose: source artifact uploaded by user.

Key fields:
- `id`
- `filename`
- `file_path`
- `content_preview`
- `content_full`
- `created_at`

### AnalysisRun

Purpose: one execution of compliance analysis.

Key fields:
- `id`
- `framework`
- `status`
- `coverage_percent`
- `risk_score`
- `summary`
- `created_at`

### Finding

Purpose: a specific control gap identified in a run.

Key fields:
- `id`
- `analysis_id`
- `title`
- `severity`
- `evidence`
- `recommendation`

### TaskItem

Purpose: remediation work item derived from findings.

Key fields:
- `id`
- `analysis_id`
- `title`
- `owner`
- `priority`
- `due_in_days`
- `status`

### Report

Purpose: persistent reference to generated report artifact.

Key fields:
- `id`
- `analysis_id`
- `report_path`
- `created_at`

## 4. API Contract Design

Design principles:
- Keep contracts explicit and frontend-friendly.
- Return predictable shapes for dashboard rendering.
- Keep analysis summary route lightweight and details route rich.

Main endpoints:
- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`
- `POST /api/v1/analysis/run`
- `GET /api/v1/analysis/{analysis_id}`
- `GET /api/v1/tasks`
- `GET /api/v1/reports/{analysis_id}`
- `GET /api/v1/reports/{analysis_id}/content`

## 5. Analysis Engine Behavior

### 5.1 Neuro-SAN path

When enabled, backend attempts Neuro-SAN orchestration and expects strict JSON output.

Advantages:
- richer semantic reasoning
- clear multi-agent architecture for judges

### 5.2 Optional deterministic local mode

If `USE_NEURO_SAN=false`, backend runs keyword-based checks across five control domains:
- ownership
- review cadence
- incident escalation
- retention
- access control

Outputs include calculated:
- coverage percentage
- weighted risk score
- findings list
- tasks list

### 5.3 Why both modes

This dual-path design allows advanced capability without sacrificing demo reliability.

## 6. Report Generation Strategy

After each run:
1. backend generates markdown report content from analysis result
2. writes file to `storage/reports`
3. stores report path in `Report` table
4. exposes metadata and full content via dedicated APIs

This provides both persistent artifact and immediate UI visibility.

## 7. Error Handling Strategy

- Missing documents for selected IDs: `404`
- Missing analysis/report records: `404`
- Missing report file: `404`
- Agent runtime/parse failures: explicit `502` in strict mode

UI-facing errors stay concise while backend remains resilient.

## 8. Performance Considerations

Current MVP is optimized for small-to-medium policy text payloads.

Potential bottlenecks for scale:
- large file uploads
- repeated full-text merges
- synchronous analysis execution on request thread

Post-MVP mitigations:
- async task queue
- chunked parsing
- result caching per document fingerprint

## 9. Security Considerations

- API keys loaded from env only
- `.env` excluded from source control
- upload directory should be scanned/sanitized in production
- auth and tenant isolation required before real-world deployment

## 10. Testing Strategy

Minimum validation included:
- health endpoint test
- compile sanity checks

Recommended additions:
- route integration tests with test DB
- deterministic analysis snapshot tests
- Neuro-SAN adapter contract tests with mocked stream output
- report generation content assertions

## 11. Extension Guide

High-value backend extensions:
1. Add framework parameterization with custom control sets.
2. Add pagination/filtering for tasks and findings.
3. Add report export formats (PDF/CSV).
4. Add audit trail for analysis execution and task updates.
5. Add user/org scoping with authentication.
