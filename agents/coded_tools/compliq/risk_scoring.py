from typing import Any
from typing import Dict

from neuro_san.interfaces.coded_tool import CodedTool


class RiskScoringTool(CodedTool):
    """Deterministic risk score normalization utility for CompliQ."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]):
        high = int(args.get("high", 0))
        medium = int(args.get("medium", 0))
        low = int(args.get("low", 0))
        total = max(1, int(args.get("total_controls", 5)))

        failed = high + medium + low
        coverage_percent = max(0.0, ((total - failed) / total) * 100)

        weighted = (high * 1.0) + (medium * 0.6) + (low * 0.3)
        risk_score = min(100.0, (weighted / total) * 100)

        return {
            "coverage_percent": round(coverage_percent, 2),
            "risk_score": round(risk_score, 2),
        }
