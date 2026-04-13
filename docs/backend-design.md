# CompliQ Backend Design

## 1. Service Boundaries

The backend service is responsible for:

1. Upload management and text capture
2. Persistence of analysis artifacts
3. Compliance scoring and finding generation
4. Report generation and lookup

## 2. Data Model

### Document

- `id`
- `filename`
- `file_path`
- `content_preview`
- `content_full`
- `created_at`

### AnalysisRun

- `id`
- `framework`
- `status`
- `coverage_percent`
- `risk_score`
- `summary`
- `created_at`

### Finding

- `id`
- `analysis_id`
- `title`
- `severity`
- `evidence`
- `recommendation`

### TaskItem

- `id`
- `analysis_id`
- `title`
- `owner`
- `priority`
- `due_in_days`
- `status`

### Report

- `id`
- `analysis_id`
- `report_path`
- `created_at`

## 3. API Contracts

### `POST /api/v1/documents/upload`

- Input: multipart file
- Output: stored document metadata

### `GET /api/v1/documents`

- Output: list of all uploaded documents

### `POST /api/v1/analysis/run`

- Input: `{ document_ids: number[], framework: string }`
- Output: analysis summary, risk and report path

### `GET /api/v1/analysis/{analysis_id}`

- Output: run metadata + findings + tasks

### `GET /api/v1/tasks`

- Optional query: `analysis_id`
- Output: task list

### `GET /api/v1/reports/{analysis_id}`

- Output: report metadata/path

## 4. Analysis Engine

The MVP includes a deterministic rule-based analyzer:

- Detects missing ownership language
- Detects missing review cadence
- Detects missing incident handling
- Detects missing retention language
- Detects missing access controls

From these controls it computes:

- Coverage percent
- Risk score
- Findings list
- Task list

## 5. Agent Extension Plan

The deterministic engine is intentionally structured for replacement by Neuro-SAN outputs:

- `run_compliance_analysis()` becomes orchestration adapter.
- Findings/tasks schemas remain stable.
- Storage and API contracts remain unchanged.
