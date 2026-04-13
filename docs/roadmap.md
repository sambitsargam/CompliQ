# CompliQ Roadmap

This roadmap extends CompliQ from hackathon MVP to deployable product.

## Phase 1: Hackathon MVP (Current)

Focus:
- prove end-to-end value quickly

Delivered:
- document ingestion
- analysis scoring and findings
- action planning tasks
- report generation and retrieval
- landing page + dashboard
- Neuro-SAN integration with deterministic fallback

Success criteria:
- complete flow demo in under 2 minutes
- clear and explainable outputs for judges

## Phase 2: Post-Hackathon Product Hardening (0-6 Weeks)

Focus:
- strengthen usability and baseline operational controls

Planned features:
1. authentication and role-based access control
2. organization workspace boundaries
3. richer document parser support (PDF/DOCX)
4. framework packs (SOC2-lite, ISO27001-lite, HIPAA-lite)
5. report export options (PDF/CSV)

Operational upgrades:
- structured logging
- API request metrics
- improved error telemetry

Success criteria:
- private beta usable by 2-3 pilot SMEs

## Phase 3: Compliance Intelligence Expansion (6-12 Weeks)

Focus:
- improve quality and explainability of analysis outputs

Planned features:
1. control-by-control evidence mapping
2. confidence scoring per finding
3. historical trend view across repeated analyses
4. remediation progress tracking dashboards
5. reviewer approval workflow before report finalization

Agent enhancements:
- framework-conditioned prompts
- domain-specific tool extensions
- guardrail validation before persistence

Success criteria:
- measurable reduction in false-positive findings
- stronger trust in generated action plans

## Phase 4: Integration and Workflow Automation (3-6 Months)

Focus:
- embed CompliQ into real SME operations

Planned integrations:
1. ticketing systems (Jira-like flow)
2. communication channels for task alerts
3. storage connectors for policy repositories
4. calendar reminders for review cycles

Workflow automation:
- automatic task creation from findings
- SLA alerts for overdue remediation
- scheduled recurring compliance scans

Success criteria:
- teams can run compliance lifecycle with minimal manual handoffs

## Phase 5: Production Readiness and Scale (6+ Months)

Focus:
- secure, multi-tenant, enterprise-grade operation

Planned capabilities:
1. tenant isolation and data governance controls
2. audit trails and immutable event history
3. managed database and backup strategy
4. queue-based asynchronous analysis processing
5. SLOs, monitoring, and incident response runbooks

Success criteria:
- production deployment with repeatable reliability and compliance evidence integrity

## Roadmap Decision Principles

When prioritizing work, CompliQ follows:
1. reliability over novelty for critical paths
2. explainability over opaque model output
3. SME utility over feature breadth
4. stable contracts over frequent breaking changes
