from pathlib import Path

from app.schemas.contracts import AnalysisResult
from app.services.agent_service import build_control_status


def build_report_content(analysis_id: int, framework: str, result: AnalysisResult) -> str:
    control_status = build_control_status(framework, result.findings)
    lines = [
        "# CompliQ Audit Summary",
        "",
        f"Analysis ID: {analysis_id}",
        f"Framework: {framework}",
        f"Compliance Coverage: {result.coverage_percent}%",
        f"Risk Score: {result.risk_score}/100",
        "",
        "## Summary",
        result.summary,
        "",
        "## Control Scorecard",
    ]

    for i, control in enumerate(control_status, start=1):
        lines.append(
            f"{i}. {control['control']}: {control['status'].upper()} "
            f"(expected severity if missing: {control['severity'].upper()})"
        )

    lines.extend(
        [
            "",
            "## Findings",
        ]
    )

    for i, finding in enumerate(result.findings, start=1):
        lines.extend(
            [
                f"{i}. {finding.title} ({finding.severity.upper()})",
                f"   - Evidence: {finding.evidence}",
                f"   - Recommendation: {finding.recommendation}",
            ]
        )

    lines.extend(["", "## Action Plan"])

    for i, task in enumerate(result.tasks, start=1):
        lines.extend(
            [
                f"{i}. {task.title}",
                f"   - Owner: {task.owner}",
                f"   - Priority: {task.priority}",
                f"   - Due in: {task.due_in_days} days",
            ]
        )

    return "\n".join(lines)


def save_report(reports_dir: str, analysis_id: int, content: str) -> str:
    Path(reports_dir).mkdir(parents=True, exist_ok=True)
    path = Path(reports_dir) / f"compliq_report_{analysis_id}.md"
    path.write_text(content, encoding="utf-8")
    return str(path)
