# CompliQ Frontend Design

## 1. Frontend Goals

The frontend is intentionally split into two modes:
1. Story mode (`/`) for quick product understanding during judging.
2. Execution mode (`/dashboard`) for live workflow demonstration.

Primary UX goals:
- communicate value in under 10 seconds
- make operational status visible
- keep core interactions simple and linear
- surface explainable outputs, not opaque model text

## 2. Route Architecture

### Route: `/`

Purpose:
- brand positioning
- feature framing
- transition user to dashboard

Content blocks:
- branded navigation
- hero with one-line value proposition
- output snapshot card (coverage/risk/gaps)
- feature cards
- call-to-action button to dashboard

### Route: `/dashboard`

Purpose:
- complete operational flow from upload to report

Main sections:
1. Workspace header
2. KPI stat cards
3. Error alert area
4. Upload and document selector panel
5. Analysis output panel (scores, findings, tasks, report)

## 3. State Model

Dashboard state categories:
- connection and platform state (`health`, API base)
- data state (`documents`, `tasks`, analysis objects)
- interaction state (`selectedDocIds`, `uploading`, `analyzing`)
- feedback state (`error`)

This separation keeps UI predictable and easy to debug.

## 4. API Client Design

`frontend/lib/api.ts` exposes narrow wrappers:
- `fetchJson`
- `postJson`
- `postFile`
- `fetchText`

Design choices:
- one base URL source (`NEXT_PUBLIC_API_BASE_URL`)
- throw errors on non-OK responses
- keep client side usage explicit and typed

## 5. Interaction Flow

### Upload flow

1. User picks file.
2. UI calls upload endpoint.
3. On success, dashboard refreshes health/docs/tasks.
4. File input resets.

### Analysis flow

1. User selects one or more documents.
2. UI calls analysis run endpoint.
3. UI fetches details by returned `analysis_id`.
4. UI fetches report content.
5. UI refreshes KPI data and task list.

## 6. Visual Direction

CompliQ UI uses:
- non-purple, enterprise-safe palette
- strong contrast for readability
- card-based information hierarchy
- soft shadows and rounded corners for polished look
- lightweight patterned background for depth

Design intent is practical credibility rather than flashy motion.

## 7. Accessibility and Readability Notes

Current MVP includes:
- large enough text for key metrics
- clear section labels
- visible button states
- straightforward linear interaction

Planned improvements:
- keyboard focus enhancements
- ARIA labeling for form inputs and cards
- contrast audits for all semantic states

## 8. Error and Empty-State Strategy

- No documents: show direct prompt to upload.
- No analysis run yet: show guidance text in output panel.
- Request failures: show inline alert with message.
- Disabled states: prevent duplicate uploads/runs while in-flight.

## 9. Component Strategy

Reusable UI building blocks:
- `StatCard`: standardized metric presentation
- `SectionCard`: consistent panel framing and spacing

These abstractions minimize CSS duplication and support incremental expansion.

## 10. Performance Considerations

Current optimizations:
- parallel initial data fetch via `Promise.all`
- selective rendering of heavy sections only when data exists

Future improvements:
- optimistic document list updates
- incremental loading for long findings/task lists
- memoization for larger data sets
- skeleton loaders for slow network demos

## 11. Future UX Enhancements

- framework selector UI and scenario templates
- severity color semantics and filtering controls
- report download/export actions
- comparison view across multiple analysis runs
- guided remediation timeline dashboard
