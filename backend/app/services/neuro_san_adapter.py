from __future__ import annotations

import json
from multiprocessing import get_context
import os
from pathlib import Path
from queue import Empty
from typing import Any

from app.core.config import get_settings
from app.schemas.contracts import AnalysisFinding
from app.schemas.contracts import AnalysisResult
from app.schemas.contracts import AnalysisTask

_LAST_NEURO_SAN_ERROR = ""


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


def _resolve_agent_paths() -> tuple[str, str]:
    settings = get_settings()
    manifest = os.environ.get("AGENT_MANIFEST_FILE") or settings.agent_manifest_file
    tools = os.environ.get("AGENT_TOOL_PATH") or settings.agent_tool_path
    return manifest, tools


def _resolve_api_key() -> str | None:
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key
    settings_key = get_settings().openai_api_key
    if settings_key:
        return settings_key
    return None


def get_neuro_san_status() -> dict[str, str | bool]:
    manifest_path, tool_path = _resolve_agent_paths()
    resolved_manifest_path = str(Path(manifest_path).resolve())
    resolved_tool_path = str(Path(tool_path).resolve())
    has_api_key = bool(_resolve_api_key())
    manifest_exists = Path(resolved_manifest_path).exists()
    tools_exist = Path(resolved_tool_path).exists()
    return {
        "enabled": True,
        "has_api_key": has_api_key,
        "manifest_path": manifest_path,
        "manifest_resolved_path": resolved_manifest_path,
        "manifest_exists": manifest_exists,
        "tool_path": tool_path,
        "tool_resolved_path": resolved_tool_path,
        "tool_path_exists": tools_exist,
        "ready": has_api_key and manifest_exists and tools_exist,
        "last_error": _LAST_NEURO_SAN_ERROR,
    }


def get_last_neuro_san_error() -> str:
    return _LAST_NEURO_SAN_ERROR


def _run_neuro_san_once(
    merged_text: str,
    framework: str,
    manifest_path: str,
    tool_path: str,
    api_key: str | None,
) -> AnalysisResult:
    from neuro_san.client.agent_session_factory import DirectAgentSessionFactory

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    os.environ["AGENT_MANIFEST_FILE"] = manifest_path
    os.environ["AGENT_TOOL_PATH"] = tool_path

    current_pythonpath = os.environ.get("PYTHONPATH", "")
    path_parts = [p for p in current_pythonpath.split(os.pathsep) if p]
    for p in [str(Path.cwd()), str(Path(tool_path).resolve())]:
        if p not in path_parts:
            path_parts.insert(0, p)
    os.environ["PYTHONPATH"] = os.pathsep.join(path_parts)

    session = DirectAgentSessionFactory().create_session(
        agent_name="compliq",
        use_direct=True,
        metadata={},
    )

    prompt = (
        "You are analyzing policy text for compliance readiness.\n"
        f"Framework: {framework}\n"
        "Return strict JSON only with keys: coverage_percent, risk_score, summary, findings, tasks.\n"
        "Text:\n"
        f"{merged_text}"
    )
    stream = session.streaming_chat({"user_message": {"text": prompt}, "sly_data": {}})
    last = None
    for msg in stream:
        last = msg
        if msg.get("done") is True:
            break

    if not last:
        raise RuntimeError("Neuro-SAN stream returned no final message.")

    text = last.get("response", {}).get("text", "")
    payload = _extract_json(text)
    if not payload:
        raise RuntimeError("Neuro-SAN response did not contain valid JSON output.")

    findings = [AnalysisFinding(**f) for f in payload.get("findings", [])]
    tasks = [AnalysisTask(**t) for t in payload.get("tasks", [])]

    return AnalysisResult(
        coverage_percent=float(payload.get("coverage_percent", 0.0)),
        risk_score=float(payload.get("risk_score", 0.0)),
        summary=str(payload.get("summary", "")),
        findings=findings,
        tasks=tasks,
    )


def _run_neuro_san_worker(
    result_queue: Any,
    merged_text: str,
    framework: str,
    manifest_path: str,
    tool_path: str,
    api_key: str | None,
) -> None:
    try:
        result = _run_neuro_san_once(
            merged_text=merged_text,
            framework=framework,
            manifest_path=manifest_path,
            tool_path=tool_path,
            api_key=api_key,
        )
        result_queue.put({"ok": True, "payload": result.model_dump()})
    except Exception as exc:
        result_queue.put({"ok": False, "error": f"{type(exc).__name__}: {exc}"})


def run_neuro_san_analysis(merged_text: str, framework: str = "SME-BASELINE") -> AnalysisResult | None:
    """
    Attempt a Neuro-SAN analysis call with a hard timeout.
    Returns None if the agent call fails.
    """
    global _LAST_NEURO_SAN_ERROR
    _LAST_NEURO_SAN_ERROR = ""

    manifest_path, tool_path = _resolve_agent_paths()
    api_key = _resolve_api_key()
    if not api_key:
        _LAST_NEURO_SAN_ERROR = "OPENAI_API_KEY is missing for strict Neuro-SAN mode."
        return None

    resolved_manifest = Path(manifest_path).resolve()
    resolved_tools = Path(tool_path).resolve()
    if not resolved_manifest.exists():
        _LAST_NEURO_SAN_ERROR = f"AGENT_MANIFEST_FILE not found: {resolved_manifest}"
        return None
    if not resolved_tools.exists():
        _LAST_NEURO_SAN_ERROR = f"AGENT_TOOL_PATH not found: {resolved_tools}"
        return None

    try:
        context = get_context("fork")
    except ValueError:
        context = get_context("spawn")
    result_queue = context.Queue(maxsize=1)
    process = context.Process(
        target=_run_neuro_san_worker,
        args=(
            result_queue,
            merged_text,
            framework,
            manifest_path,
            tool_path,
            api_key,
        ),
    )
    process.start()
    process.join(timeout=45)

    if process.is_alive():
        process.terminate()
        process.join(timeout=2)
        _LAST_NEURO_SAN_ERROR = "Timed out after 45s waiting for Neuro-SAN response."
        return None

    message: dict[str, Any]
    try:
        message = result_queue.get_nowait()
    except Empty:
        if process.exitcode not in (0, None):
            _LAST_NEURO_SAN_ERROR = f"Neuro-SAN worker exited with code {process.exitcode}."
        else:
            _LAST_NEURO_SAN_ERROR = "Neuro-SAN worker produced no output."
        return None
    finally:
        result_queue.close()
        result_queue.join_thread()

    if not message.get("ok"):
        _LAST_NEURO_SAN_ERROR = str(message.get("error") or "Unknown Neuro-SAN worker error.")
        return None

    payload = message.get("payload")
    if not isinstance(payload, dict):
        _LAST_NEURO_SAN_ERROR = "Neuro-SAN worker returned an invalid payload format."
        return None

    try:
        findings = [AnalysisFinding(**f) for f in payload.get("findings", [])]
        tasks = [AnalysisTask(**t) for t in payload.get("tasks", [])]
        return AnalysisResult(
            coverage_percent=float(payload.get("coverage_percent", 0.0)),
            risk_score=float(payload.get("risk_score", 0.0)),
            summary=str(payload.get("summary", "")),
            findings=findings,
            tasks=tasks,
        )
    except Exception as exc:
        _LAST_NEURO_SAN_ERROR = f"Invalid Neuro-SAN payload: {type(exc).__name__}: {exc}"
        return None
