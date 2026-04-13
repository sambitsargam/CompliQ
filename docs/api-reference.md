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

## 3. Analysis

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
  "report_path": "./storage/reports/compliq_report_9.md"
}
```

Common errors:
- `404` with `"No documents found for given IDs"` when IDs are invalid
- `422` when request shape is invalid

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
  ]
}
```

Common errors:
- `404` with `"Analysis not found"`

## 4. Tasks

### `GET /api/v1/tasks`

Purpose:
- list tasks across all runs or for one analysis run

Optional query params:
- `analysis_id` (integer)

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

## 5. Reports

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

## 6. Error Format

FastAPI default error payload shape:

```json
{
  "detail": "Error message"
}
```

Validation errors (`422`) follow FastAPI validation structure.

## 7. Contract Stability Notes

Stable fields expected by current frontend:
- analysis summary keys from `/analysis/run`
- nested `analysis`, `findings`, `tasks` from `/analysis/{id}`
- text payload from `/reports/{id}/content`

If backend contracts change, frontend `lib/api.ts` and dashboard state types must be updated in same commit.
