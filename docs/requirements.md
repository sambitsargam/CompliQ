# CompliQ Requirements Specification

## 1. Context and Problem Statement

Small and medium businesses need affordable compliance readiness support but usually lack dedicated legal-ops tooling. Policies are often stored as disconnected documents, making it hard to answer:
- What controls are currently documented?
- What gaps create risk?
- What should be fixed first?

CompliQ solves this by turning raw policy text into structured, explainable compliance outputs.

## 2. Product Goals

Primary goals for hackathon MVP:
1. Deliver a complete upload-to-report workflow.
2. Provide interpretable outputs (evidence + recommendations).
3. Demonstrate agentic orchestration with Neuro-SAN.
4. Preserve runtime reliability through deterministic fallback.
5. Keep local setup simple (no Docker requirement).

## 3. Stakeholders

- SME founder or operator (decision maker)
- Compliance lead or operations manager (primary user)
- Hackathon judges (evaluation audience)

## 4. Functional Requirements

### FR-1 Document Ingestion

- User can upload text-based policy artifacts.
- System stores metadata, full text, and preview snippet.
- System exposes uploaded records via list endpoint.

Acceptance criteria:
- Upload API returns document ID and timestamp.
- Document appears in dashboard list without restart.

### FR-2 Analysis Request

- User selects one or more uploaded document IDs.
- User triggers analysis with framework tag (default `SME-BASELINE`).
- System merges selected text and processes it.

Acceptance criteria:
- Invalid IDs return explicit `404`.
- Valid IDs return analysis summary with scores.

### FR-3 Findings Generation

For each gap finding, system returns:
- title
- severity (`high`, `medium`, `low`)
- evidence summary
- recommendation

Acceptance criteria:
- Each finding has non-empty evidence and recommendation text.

### FR-4 Remediation Task Generation

For each finding, system returns an action task with:
- title
- owner
- priority (`P1`, `P2`, `P3`)
- due window (`due_in_days`)
- status (default `open` in persistence)

Acceptance criteria:
- Findings and tasks are consistently linked by analysis run.

### FR-5 Report Artifact Generation

- System generates a report artifact per analysis run.
- Report must include summary, scores, findings, and tasks.

Acceptance criteria:
- Report metadata is queryable via API.
- Report content is retrievable as text.

### FR-6 Dashboard Read and Interaction

Dashboard must support:
- Health status visibility
- Document list and selection
- Analysis trigger
- Findings and tasks rendering
- Report content rendering

Acceptance criteria:
- Full flow is executable through UI only.

## 5. Non-Functional Requirements

### NFR-1 Setup Speed

- Local run should be possible in under 15 minutes.
- No Docker dependency for MVP.

### NFR-2 Explainability

- Outputs must remain understandable to non-technical users.
- Findings should include evidence and corrective direction.

### NFR-3 Reliability

- System must return output even if agent path fails.
- Fallback behavior should be deterministic for same input.

### NFR-4 Security Hygiene

- Secrets must not be committed.
- `.env` must remain ignored by git.
- `.env.example` must contain placeholders only.

### NFR-5 Demo Readiness

- APIs must be stable enough for repeat live demo runs.
- UI must clearly communicate run status and outputs.

## 6. Technical Requirements

- Backend: FastAPI, SQLModel, SQLite
- Frontend: Next.js, TypeScript, Tailwind CSS
- Agent Layer: Neuro-SAN with coded tools
- Configuration: `.env` loaded via pydantic settings

## 7. Out of Scope (MVP)

- User authentication and RBAC
- Multi-tenant org boundaries
- Full legal citation tracing
- Enterprise integrations (SIEM, ERP, ticketing)
- Advanced file parsing for all binary formats

## 8. Risks and Mitigations

1. LLM/agent instability
- Mitigation: deterministic fallback engine

2. Time-limited hackathon execution
- Mitigation: strict MVP boundaries and incremental delivery

3. Demo failure due to environment issues
- Mitigation: runbook, health checks, and local-first defaults

## 9. Success Metrics

Hackathon-relevant success indicators:
- End-to-end flow executes live in under 2 minutes
- At least one meaningful finding generated for weak sample input
- Clear remediation tasks produced with priorities
- Report artifact generated and visible
- Architecture and docs are judge-consumable
