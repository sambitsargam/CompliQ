# CompliQ Submission Checklist

Use this checklist before final hackathon submission.

## 1. Product Readiness

- [ ] Landing page clearly explains problem and solution.
- [ ] Dashboard performs upload -> analyze -> report flow.
- [ ] Findings include severity, evidence, and recommendation.
- [ ] Tasks include owner, priority, and due window.
- [ ] Report content is visible and coherent.

## 2. Technical Readiness

- [ ] Backend starts and `/health` returns `ok`.
- [ ] Frontend connects to backend without CORS issues.
- [ ] SQLite persistence works across multiple runs.
- [ ] Neuro-SAN path configured (or fallback confirmed working).
- [ ] `.env` ignored and `.env.example` present.

## 3. Documentation Readiness

- [ ] Root README includes full setup and run steps.
- [ ] `docs/architecture.md` explains components and data flow.
- [ ] `docs/api-reference.md` reflects actual endpoint contracts.
- [ ] `docs/runbook.md` supports a reproducible live demo.
- [ ] `docs/development-plan.md` reflects implementation phases.

## 4. Judging Evidence Mapping

Prepare explicit proof points for likely evaluation categories.

### Innovation / Agentic Design

Evidence:
- Neuro-SAN multi-agent topology in `agents/`
- frontman + specialist + coded tools architecture
- strict structured output contract

### Implementation Quality

Evidence:
- full-stack working product
- persistent backend models and APIs
- polished dashboard with end-to-end flow

### Practical Impact

Evidence:
- SME compliance pain-point focus
- actionable remediation tasks, not only scores
- audit-style report generation

### Reliability and Demo Strength

Evidence:
- deterministic fallback path
- documented runbook and troubleshooting
- stable local setup without Docker dependency

## 5. Mandatory Artifacts

- [ ] Public source repository URL
- [ ] Working prototype demo
- [ ] Architecture/design documentation
- [ ] 1-2 page solution summary
- [ ] Short demo video

## 6. Demo Video Checklist

- [ ] Duration kept concise (typically 2-4 minutes)
- [ ] Shows real upload and analysis execution
- [ ] Narrates output interpretation (coverage/risk/findings/tasks)
- [ ] Mentions agentic architecture and fallback reliability
- [ ] Ends with impact statement for SMEs

## 7. Final Quality Gate (Last 30 Minutes)

- [ ] Pull latest code on demo machine
- [ ] Run backend and frontend fresh
- [ ] Perform one full smoke test
- [ ] Confirm no hardcoded keys in codebase
- [ ] Keep sample document ready for live walkthrough
- [ ] Keep backup recording ready in case of network issues
