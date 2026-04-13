from __future__ import annotations

from typing import Any, Literal

from app.core.config import get_settings
from app.schemas.contracts import AnalysisFinding, AnalysisResult, AnalysisTask
from app.services.neuro_san_adapter import get_last_neuro_san_error, run_neuro_san_analysis


FrameworkId = Literal["SME-BASELINE", "DATA-PRIVACY", "INCIDENT-READY"]


def _normalize_framework(framework: str) -> FrameworkId:
    value = framework.strip().upper()
    if value in {"SME-BASELINE", "DATA-PRIVACY", "INCIDENT-READY"}:
        return value  # type: ignore[return-value]
    return "SME-BASELINE"


def get_supported_frameworks() -> list[dict[str, str]]:
    return [
        {
            "id": "SME-BASELINE",
            "label": "SME Baseline",
            "tagline": "Balanced controls for policy ownership, reviews, incidents, retention, and access.",
        },
        {
            "id": "DATA-PRIVACY",
            "label": "Data Privacy",
            "tagline": "Focused on personal data lifecycle, rights handling, and protection controls.",
        },
        {
            "id": "INCIDENT-READY",
            "label": "Incident Ready",
            "tagline": "Focused on escalation, response playbooks, communication, and recovery readiness.",
        },
    ]


def _framework_checks(framework: str) -> list[dict[str, str | list[str]]]:
    normalized = _normalize_framework(framework)

    if normalized == "DATA-PRIVACY":
        return [
            {
                "control": "Data Inventory & Classification",
                "missing_title": "Data inventory is not defined",
                "severity": "high",
                "evidence": "No clear inventory/classification keywords found (inventory/classification/personal data).",
                "recommendation": "Add data inventory with classification labels and ownership.",
                "keywords": ["inventory", "classification", "personal data", "pii"],
            },
            {
                "control": "Consent or Legal Basis",
                "missing_title": "Lawful basis or consent handling missing",
                "severity": "high",
                "evidence": "No legal-basis keywords found (consent/lawful basis/legitimate interest).",
                "recommendation": "Document consent/legal basis for each major data processing activity.",
                "keywords": ["consent", "lawful basis", "legitimate interest"],
            },
            {
                "control": "Retention & Deletion",
                "missing_title": "Retention lifecycle is undefined",
                "severity": "medium",
                "evidence": "No retention lifecycle keywords found (retention/delete/archive).",
                "recommendation": "Define retention durations with deletion/archive workflows.",
                "keywords": ["retention", "delete", "archive"],
            },
            {
                "control": "Data Subject Rights Workflow",
                "missing_title": "Data subject request workflow missing",
                "severity": "medium",
                "evidence": "No data-rights keywords found (request/erasure/access/rectification).",
                "recommendation": "Create a workflow for access, correction, and deletion requests.",
                "keywords": ["request", "erasure", "access request", "rectification"],
            },
            {
                "control": "Protection Controls",
                "missing_title": "Protection controls are weak",
                "severity": "medium",
                "evidence": "No protection keywords found (encryption/access/permission).",
                "recommendation": "Define encryption and role-based protection controls.",
                "keywords": ["encryption", "access", "permission", "role"],
            },
        ]

    if normalized == "INCIDENT-READY":
        return [
            {
                "control": "Incident Escalation Matrix",
                "missing_title": "Incident escalation path is undefined",
                "severity": "high",
                "evidence": "No escalation keywords found (incident/escalation/severity).",
                "recommendation": "Define an escalation matrix with severity levels and owners.",
                "keywords": ["incident", "escalation", "severity"],
            },
            {
                "control": "Response Playbook",
                "missing_title": "Response playbook is missing",
                "severity": "high",
                "evidence": "No response playbook keywords found (playbook/containment/triage).",
                "recommendation": "Publish a response playbook for triage and containment.",
                "keywords": ["playbook", "containment", "triage"],
            },
            {
                "control": "Breach Communication",
                "missing_title": "Breach communication workflow missing",
                "severity": "medium",
                "evidence": "No communication keywords found (notify/report/stakeholder).",
                "recommendation": "Define internal and external breach notification protocol.",
                "keywords": ["notify", "report", "stakeholder", "communication"],
            },
            {
                "control": "Post-Incident RCA",
                "missing_title": "Post-incident RCA process not defined",
                "severity": "medium",
                "evidence": "No root-cause keywords found (postmortem/root cause/lessons learned).",
                "recommendation": "Add post-incident RCA and lessons-learned process.",
                "keywords": ["postmortem", "root cause", "lessons learned"],
            },
            {
                "control": "Recovery Testing",
                "missing_title": "Recovery testing and drills are unclear",
                "severity": "medium",
                "evidence": "No recovery-test keywords found (recovery/drill/backup restore).",
                "recommendation": "Define periodic recovery drills and backup restore testing.",
                "keywords": ["recovery", "drill", "backup", "restore"],
            },
        ]

    return [
        {
            "control": "Policy Ownership",
            "missing_title": "Policy ownership missing",
            "severity": "high",
            "evidence": "No clear owner keyword found (owner/responsible).",
            "recommendation": "Assign a compliance owner and include owner details in policy docs.",
            "keywords": ["owner", "responsible", "accountable"],
        },
        {
            "control": "Review Cycle",
            "missing_title": "Review cycle undefined",
            "severity": "medium",
            "evidence": "No review cadence keyword found (review/annual/quarterly).",
            "recommendation": "Add a periodic policy review cycle with explicit dates.",
            "keywords": ["review", "annual", "quarterly"],
        },
        {
            "control": "Incident Escalation",
            "missing_title": "Incident escalation not documented",
            "severity": "high",
            "evidence": "No incident escalation keyword found (incident/escalation/breach).",
            "recommendation": "Document incident escalation, breach handling, and escalation matrix.",
            "keywords": ["incident", "escalation", "breach"],
        },
        {
            "control": "Data Retention",
            "missing_title": "Data retention clause unclear",
            "severity": "medium",
            "evidence": "No retention keyword found (retention/archive/delete).",
            "recommendation": "Define retention duration and deletion/archive workflow.",
            "keywords": ["retention", "archive", "delete"],
        },
        {
            "control": "Access Governance",
            "missing_title": "Access control language weak",
            "severity": "medium",
            "evidence": "No access-control keyword found (access/role/permission).",
            "recommendation": "Add role-based access and least-privilege controls.",
            "keywords": ["access", "role", "permission"],
        },
    ]


def build_control_status(framework: str, findings: list[Any]) -> list[dict[str, str]]:
    missing_titles: set[str] = set()
    for finding in findings:
        title = getattr(finding, "title", None)
        if title is None and isinstance(finding, dict):
            title = finding.get("title")
        if isinstance(title, str) and title.strip():
            missing_titles.add(title.strip().lower())
    statuses: list[dict[str, str]] = []

    for check in _framework_checks(framework):
        gap_title = str(check["missing_title"])
        has_gap = gap_title.lower() in missing_titles
        statuses.append(
            {
                "control": str(check["control"]),
                "status": "gap" if has_gap else "pass",
                "severity": str(check["severity"]),
                "gap_title": gap_title if has_gap else "",
            }
        )

    return statuses


def _heuristic_analysis(merged_text: str, framework: str) -> AnalysisResult:
    checks = _framework_checks(framework)

    lowered = merged_text.lower()
    findings: list[AnalysisFinding] = []

    for check in checks:
        keywords = [str(keyword) for keyword in check["keywords"]]
        if not any(keyword in lowered for keyword in keywords):
            findings.append(
                AnalysisFinding(
                    title=str(check["missing_title"]),
                    severity=str(check["severity"]),
                    evidence=str(check["evidence"]),
                    recommendation=str(check["recommendation"]),
                )
            )

    total_controls = len(checks)
    failed_controls = len(findings)
    coverage = max(0.0, ((total_controls - failed_controls) / total_controls) * 100)

    severity_weight = {"high": 1.0, "medium": 0.6, "low": 0.3}
    weighted_risk = sum(severity_weight.get(f.severity, 0.3) for f in findings)
    risk_score = round(min(100.0, (weighted_risk / total_controls) * 100), 2)

    tasks = [
        AnalysisTask(
            title=f"Resolve: {f.title}",
            owner="Compliance Owner",
            priority="P1" if f.severity == "high" else "P2",
            due_in_days=7 if f.severity == "high" else 14,
        )
        for f in findings
    ]

    summary = (
        f"CompliQ analyzed the {_normalize_framework(framework)} framework and found {failed_controls} control gaps. "
        f"Coverage is {coverage:.1f}%, with risk score {risk_score:.1f}/100."
    )

    return AnalysisResult(
        coverage_percent=round(coverage, 2),
        risk_score=risk_score,
        summary=summary,
        findings=findings,
        tasks=tasks,
    )


def run_compliance_analysis(merged_text: str, framework: str = "SME-BASELINE") -> AnalysisResult:
    settings = get_settings()

    if settings.use_neuro_san:
        neuro_result = run_neuro_san_analysis(merged_text, framework=framework)
        if neuro_result is not None:
            return neuro_result
        raise RuntimeError(get_last_neuro_san_error() or "Neuro-SAN failed in strict mode.")

    return _heuristic_analysis(merged_text, framework)
