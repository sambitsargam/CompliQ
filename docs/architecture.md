# CompliQ Architecture

## High-Level Components

1. Frontend (Next.js): landing page and dashboard.
2. Backend (FastAPI): APIs for documents, analysis, tasks, reports.
3. Agent Layer (Neuro-SAN): multi-agent compliance workflow.
4. Storage (SQLite): metadata, findings, tasks, reports.

## Agent Workflow

1. ComplianceFrontman receives analysis request.
2. DocParser extracts obligations and evidence.
3. RuleMapper maps evidence to controls/checklists.
4. GapDetector identifies missing controls.
5. RiskScorer assigns severity and confidence.
6. ActionPlanner creates remediation tasks.
7. ReportAgent formats an audit-ready summary.
