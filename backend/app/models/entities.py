from datetime import datetime

from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str
    file_path: str
    content_preview: str
    content_full: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AnalysisRun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    framework: str = "SME-BASELINE"
    status: str = "completed"
    coverage_percent: float = 0.0
    risk_score: float = 0.0
    summary: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Finding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    analysis_id: int = Field(index=True)
    title: str
    severity: str
    evidence: str
    recommendation: str


class TaskItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    analysis_id: int = Field(index=True)
    title: str
    owner: str = "Compliance Owner"
    priority: str
    due_in_days: int
    status: str = "open"


class Report(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    analysis_id: int = Field(index=True)
    report_path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
