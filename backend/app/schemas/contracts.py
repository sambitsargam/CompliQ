from pydantic import BaseModel


class AnalysisRunRequest(BaseModel):
    document_ids: list[int]
    framework: str = "SME-BASELINE"


class AnalysisFinding(BaseModel):
    title: str
    severity: str
    evidence: str
    recommendation: str


class AnalysisTask(BaseModel):
    title: str
    owner: str
    priority: str
    due_in_days: int


class AnalysisResult(BaseModel):
    coverage_percent: float
    risk_score: float
    summary: str
    findings: list[AnalysisFinding]
    tasks: list[AnalysisTask]
