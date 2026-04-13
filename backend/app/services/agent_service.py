from __future__ import annotations

from app.core.config import get_settings
from app.schemas.contracts import AnalysisFinding, AnalysisResult, AnalysisTask
from app.services.neuro_san_adapter import run_neuro_san_analysis


def _heuristic_analysis(merged_text: str) -> AnalysisResult:
    checks = [
        (
            "Policy ownership missing",
            "high",
            "No clear owner keyword found (owner/responsible).",
            "Assign a compliance owner and include owner details in policy docs.",
            ["owner", "responsible", "accountable"],
        ),
        (
            "Review cycle undefined",
            "medium",
            "No review cadence keyword found (review/annual/quarterly).",
            "Add a periodic policy review cycle with explicit dates.",
            ["review", "annual", "quarterly"],
        ),
        (
            "Incident escalation not documented",
            "high",
            "No incident escalation keyword found (incident/escalation/breach).",
            "Document incident escalation, breach handling, and escalation matrix.",
            ["incident", "escalation", "breach"],
        ),
        (
            "Data retention clause unclear",
            "medium",
            "No retention keyword found (retention/archive/delete).",
            "Define retention duration and deletion/archive workflow.",
            ["retention", "archive", "delete"],
        ),
        (
            "Access control language weak",
            "medium",
            "No access-control keyword found (access/role/permission).",
            "Add role-based access and least-privilege controls.",
            ["access", "role", "permission"],
        ),
    ]

    lowered = merged_text.lower()
    findings: list[AnalysisFinding] = []

    for title, severity, evidence, recommendation, keywords in checks:
        if not any(k in lowered for k in keywords):
            findings.append(
                AnalysisFinding(
                    title=title,
                    severity=severity,
                    evidence=evidence,
                    recommendation=recommendation,
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
        f"CompliQ scanned policy artifacts and found {failed_controls} control gaps. "
        f"Coverage is {coverage:.1f}%, with risk score {risk_score:.1f}/100."
    )

    return AnalysisResult(
        coverage_percent=round(coverage, 2),
        risk_score=risk_score,
        summary=summary,
        findings=findings,
        tasks=tasks,
    )


def run_compliance_analysis(merged_text: str) -> AnalysisResult:
    settings = get_settings()

    if settings.use_neuro_san:
        neuro_result = run_neuro_san_analysis(merged_text)
        if neuro_result is not None:
            return neuro_result

    return _heuristic_analysis(merged_text)
