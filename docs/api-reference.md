# CompliQ API Reference

Base URL (local): `http://localhost:8000`

All examples below use local development assumptions.

## 1. Health Endpoints

### `GET /health`

Purpose:
- root service heartbeat

Success response (`200`):

```json
{
  "status": "ok",
  "service": "CompliQ API"
}
```

### `GET /api/v1/health`

Purpose:
- versioned health route from router

Success response (`200`):
- same payload shape as `/health`

## 2. Documents

### `POST /api/v1/documents/upload`

Purpose:
- upload one document and persist metadata/content

Content-Type:
- `multipart/form-data`

Form fields:
- `file` (required)

Success response (`200`):

```json
{
  "id": 1,
  "filename": "policy.txt",
  "preview": "Policy owner is...",
  "created_at": "2026-04-13T12:00:00"
}
```

Common errors:
- `422` when file form field is missing

### `GET /api/v1/documents`

Purpose:
- list all uploaded documents (newest first)

Success response (`200`):

```json
[
  {
    "id": 1,
    "filename": "policy.txt",
    "file_path": "./storage/uploads/policy.txt",
    "content_preview": "Policy owner is...",
    "content_full": "...",
    "created_at": "2026-04-13T12:00:00"
  }
]
```

## 3. Frameworks and Agent Readiness

### `GET /api/v1/frameworks`

Purpose:
- list available framework packs supported by analyzer

Success response (`200`):

```json
[
  {
    "id": "SME-BASELINE",
    "label": "SME Baseline",
    "tagline": "Balanced controls for policy ownership, reviews, incidents, retention, and access."
  },
  {
    "id": "DATA-PRIVACY",
    "label": "Data Privacy",
    "tagline": "Focused on personal data lifecycle, rights handling, and protection controls."
  }
]
```

### `GET /api/v1/neuro-san/status`

Purpose:
- return Neuro-SAN readiness signal for safe runtime handling

Success response (`200`):

```json
{
  "enabled": true,
  "has_api_key": false,
  "manifest_path": ".../agents/registries/manifest.hocon",
  "manifest_exists": true,
  "tool_path": ".../agents/coded_tools",
  "tool_path_exists": true,
  "ready": false
}
```

`ready=false` means Neuro-SAN-required runs will fail with `502` until configuration is complete.

## 4. Analysis

### `POST /api/v1/analysis/run`

Purpose:
- run compliance analysis for selected document IDs

Request body:

```json
{
  "document_ids": [1, 2],
  "framework": "SME-BASELINE"
}
```

Success response (`200`):

```json
{
  "analysis_id": 9,
  "coverage_percent": 72.0,
  "risk_score": 64.0,
  "summary": "CompliQ scanned policy artifacts...",
  "findings_count": 3,
  "tasks_count": 3,
  "report_path": "./storage/reports/compliq_report_9.md",
  "control_status": [
    {
      "control": "Policy Ownership",
      "status": "gap",
      "severity": "high",
      "gap_title": "Policy ownership missing"
    }
  ]
}
```

Common errors:
- `404` with `"No documents found for given IDs"` when IDs are invalid
- `422` when request shape is invalid

### `GET /api/v1/analysis`

Purpose:
- list recent analysis runs (for dashboard history)

Optional query params:
- `limit` (1-100, default 20)

### `GET /api/v1/analysis/{analysis_id}`

Purpose:
- fetch full analysis artifact set

Path params:
- `analysis_id` (integer)

Success response (`200`):

```json
{
  "analysis": {
    "id": 9,
    "framework": "SME-BASELINE",
    "status": "completed",
    "coverage_percent": 72.0,
    "risk_score": 64.0,
    "summary": "...",
    "created_at": "2026-04-13T12:15:00"
  },
  "findings": [
    {
      "id": 1,
      "analysis_id": 9,
      "title": "Policy ownership missing",
      "severity": "high",
      "evidence": "...",
      "recommendation": "..."
    }
  ],
  "tasks": [
    {
      "id": 1,
      "analysis_id": 9,
      "title": "Resolve: Policy ownership missing",
      "owner": "Compliance Owner",
      "priority": "P1",
      "due_in_days": 7,
      "status": "open"
    }
  ],
  "control_status": [
    {
      "control": "Policy Ownership",
      "status": "gap",
      "severity": "high",
      "gap_title": "Policy ownership missing"
    }
  ]
}
```

Common errors:
- `404` with `"Analysis not found"`

## 5. Tasks

### `GET /api/v1/tasks`

Purpose:
- list tasks across all runs or for one analysis run

Optional query params:
- `analysis_id` (integer)
- `status` (`open`, `in_progress`, `done`)

Success response (`200`):

```json
[
  {
    "id": 1,
    "analysis_id": 9,
    "title": "Resolve: Policy ownership missing",
    "owner": "Compliance Owner",
    "priority": "P1",
    "due_in_days": 7,
    "status": "open"
  }
]
```

### `PATCH /api/v1/tasks/{task_id}`

Purpose:
- update task status for workflow execution

Request body:

```json
{
  "status": "in_progress"
}
```

Allowed status values:
- `open`
- `in_progress`
- `done`

## 6. Reports

### `GET /api/v1/reports/{analysis_id}`

Purpose:
- fetch report metadata row for an analysis

Success response (`200`):

```json
{
  "id": 1,
  "analysis_id": 9,
  "report_path": "./storage/reports/compliq_report_9.md",
  "created_at": "2026-04-13T12:15:10"
}
```

Common errors:
- `404` with `"Report not found"`

### `GET /api/v1/reports/{analysis_id}/content`

Purpose:
- fetch report file contents as plain text

Success response (`200`):
- content type: `text/plain`
- body: markdown report text

Common errors:
- `404` with `"Report not found"`
- `404` with `"Report file missing"`

### `GET /api/v1/reports/{analysis_id}/download`

Purpose:
- download generated markdown report as attachment

Success response (`200`):
- content type: `text/markdown`
- includes `Content-Disposition: attachment; filename="compliq_report_<id>.md"`

## 7. Error Format

FastAPI default error payload shape:

```json
{
  "detail": "Error message"
}
```

Validation errors (`422`) follow FastAPI validation structure.

## 8. Contract Stability Notes

Stable fields expected by current frontend:
- analysis summary keys from `/analysis/run`
- nested `analysis`, `findings`, `tasks`, `control_status` from `/analysis/{id}`
- text payload from `/reports/{id}/content`

If backend contracts change, frontend `lib/api.ts` and dashboard state types must be updated in same commit.
