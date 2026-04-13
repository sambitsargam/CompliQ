from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, PlainTextResponse
from sqlmodel import Session, select

from app.core.config import get_settings
from app.core.database import get_session
from app.models.entities import AnalysisRun, Document, Finding, Report, TaskItem
from app.schemas.contracts import AnalysisRunRequest, TaskUpdateRequest
from app.services.agent_service import build_control_status, get_supported_frameworks, run_compliance_analysis
from app.services.document_service import save_upload, safe_preview
from app.services.neuro_san_adapter import get_neuro_san_status
from app.services.report_service import build_report_content, save_report

router = APIRouter(prefix="/api/v1", tags=["compliq"])


@router.get("/health")
def health():
    return {"status": "ok", "service": "CompliQ API"}


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    settings = get_settings()
    filename, path, text = await save_upload(file, settings.upload_dir)

    doc = Document(
        filename=filename,
        file_path=path,
        content_preview=safe_preview(text),
        content_full=text,
    )
    session.add(doc)
    session.commit()
    session.refresh(doc)

    return {
        "id": doc.id,
        "filename": doc.filename,
        "preview": doc.content_preview,
        "created_at": doc.created_at,
    }


@router.get("/documents")
def list_documents(session: Session = Depends(get_session)):
    docs = session.exec(select(Document).order_by(Document.created_at.desc())).all()
    return docs


@router.get("/frameworks")
def list_frameworks():
    return get_supported_frameworks()


@router.get("/neuro-san/status")
def neuro_san_status():
    return get_neuro_san_status()


@router.post("/analysis/run")
def run_analysis(payload: AnalysisRunRequest, session: Session = Depends(get_session)):
    docs = session.exec(select(Document).where(Document.id.in_(payload.document_ids))).all()
    if not docs:
        raise HTTPException(status_code=404, detail="No documents found for given IDs")

    merged_text = "\n\n".join(doc.content_full for doc in docs)
    try:
        result = run_compliance_analysis(merged_text, payload.framework)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=f"Neuro-SAN failed: {exc}") from exc
    control_status = build_control_status(payload.framework, result.findings)

    analysis = AnalysisRun(
        framework=payload.framework,
        coverage_percent=result.coverage_percent,
        risk_score=result.risk_score,
        summary=result.summary,
    )
    session.add(analysis)
    session.commit()
    session.refresh(analysis)

    for finding in result.findings:
        session.add(
            Finding(
                analysis_id=analysis.id,
                title=finding.title,
                severity=finding.severity,
                evidence=finding.evidence,
                recommendation=finding.recommendation,
            )
        )

    for task in result.tasks:
        session.add(
            TaskItem(
                analysis_id=analysis.id,
                title=task.title,
                owner=task.owner,
                priority=task.priority,
                due_in_days=task.due_in_days,
            )
        )

    report_content = build_report_content(analysis.id, payload.framework, result)
    report_path = save_report(get_settings().reports_dir, analysis.id, report_content)
    session.add(Report(analysis_id=analysis.id, report_path=report_path))

    session.commit()

    return {
        "analysis_id": analysis.id,
        "coverage_percent": analysis.coverage_percent,
        "risk_score": analysis.risk_score,
        "summary": analysis.summary,
        "findings_count": len(result.findings),
        "tasks_count": len(result.tasks),
        "report_path": report_path,
        "control_status": control_status,
    }


@router.get("/analysis")
def list_analysis_runs(limit: int = 20, session: Session = Depends(get_session)):
    safe_limit = min(max(limit, 1), 100)
    query = select(AnalysisRun).order_by(AnalysisRun.created_at.desc()).limit(safe_limit)
    return session.exec(query).all()


@router.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: int, session: Session = Depends(get_session)):
    analysis = session.get(AnalysisRun, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    findings = session.exec(select(Finding).where(Finding.analysis_id == analysis_id)).all()
    tasks = session.exec(select(TaskItem).where(TaskItem.analysis_id == analysis_id)).all()
    control_status = build_control_status(analysis.framework, findings)

    return {
        "analysis": analysis,
        "findings": findings,
        "tasks": tasks,
        "control_status": control_status,
    }


@router.get("/tasks")
def list_tasks(
    analysis_id: int | None = None,
    status: str | None = None,
    session: Session = Depends(get_session),
):
    query = select(TaskItem)
    if analysis_id is not None:
        query = query.where(TaskItem.analysis_id == analysis_id)
    if status is not None:
        query = query.where(TaskItem.status == status)
    query = query.order_by(TaskItem.id.desc())
    return session.exec(query).all()


@router.patch("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdateRequest, session: Session = Depends(get_session)):
    task = session.get(TaskItem, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = payload.status
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/reports/{analysis_id}")
def get_report(analysis_id: int, session: Session = Depends(get_session)):
    report = session.exec(select(Report).where(Report.analysis_id == analysis_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/reports/{analysis_id}/content", response_class=PlainTextResponse)
def get_report_content(analysis_id: int, session: Session = Depends(get_session)):
    report = session.exec(select(Report).where(Report.analysis_id == analysis_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report_path = Path(report.report_path)
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report file missing")

    return report_path.read_text(encoding="utf-8")


@router.get("/reports/{analysis_id}/download")
def download_report(analysis_id: int, session: Session = Depends(get_session)):
    report = session.exec(select(Report).where(Report.analysis_id == analysis_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report_path = Path(report.report_path)
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report file missing")

    return FileResponse(
        path=report_path,
        media_type="text/markdown",
        filename=report_path.name,
    )
