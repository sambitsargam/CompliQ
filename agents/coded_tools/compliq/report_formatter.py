from typing import Any
from typing import Dict

from neuro_san.interfaces.coded_tool import CodedTool


class ReportFormatterTool(CodedTool):
    """Formats final compliance output shape."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]):
        return {
            "coverage_percent": float(args.get("coverage_percent", 0.0)),
            "risk_score": float(args.get("risk_score", 0.0)),
            "summary": str(args.get("summary", "")),
            "findings": list(args.get("findings", [])),
            "tasks": list(args.get("tasks", [])),
        }
