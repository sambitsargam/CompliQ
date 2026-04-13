from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.schemas.contracts import AnalysisFinding
from app.schemas.contracts import AnalysisResult
from app.schemas.contracts import AnalysisTask


def _extract_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    if not text:
        return None

    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return None
    return None


def run_neuro_san_analysis(merged_text: str) -> AnalysisResult | None:
    """
    Attempt a Neuro-SAN analysis call.
    Returns None if the agent call fails, so caller can fallback gracefully.
    """
    try:
        from neuro_san.client.agent_session_factory import DirectAgentSessionFactory

        cwd = Path.cwd()
        default_manifest = str((cwd.parent / "agents" / "registries" / "manifest.hocon").resolve())
        default_tools = str((cwd.parent / "agents" / "coded_tools").resolve())

        os.environ.setdefault("AGENT_MANIFEST_FILE", default_manifest)
        os.environ.setdefault("AGENT_TOOL_PATH", default_tools)

        current_pythonpath = os.environ.get("PYTHONPATH", "")
        path_parts = [p for p in current_pythonpath.split(os.pathsep) if p]
        for p in [str(cwd), str((cwd.parent / "agents" / "coded_tools").resolve())]:
            if p not in path_parts:
                path_parts.insert(0, p)
        os.environ["PYTHONPATH"] = os.pathsep.join(path_parts)

        session = DirectAgentSessionFactory().create_session(
            agent_name="compliq",
            use_direct=True,
            metadata={},
        )

        stream = session.streaming_chat({"user_message": {"text": merged_text}, "sly_data": {}})
        last = None
        for msg in stream:
            last = msg
            if msg.get("done") is True:
                break

        if not last:
            return None

        text = last.get("response", {}).get("text", "")
        payload = _extract_json(text)
        if not payload:
            return None

        findings = [AnalysisFinding(**f) for f in payload.get("findings", [])]
        tasks = [AnalysisTask(**t) for t in payload.get("tasks", [])]

        return AnalysisResult(
            coverage_percent=float(payload.get("coverage_percent", 0.0)),
            risk_score=float(payload.get("risk_score", 0.0)),
            summary=str(payload.get("summary", "")),
            findings=findings,
            tasks=tasks,
        )
    except Exception:
        return None
