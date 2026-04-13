"use client";

import { useEffect, useMemo, useState } from "react";

import { SectionCard } from "@/components/section-card";
import { StatCard } from "@/components/stat-card";
import { API_BASE_URL, fetchJson, fetchText, patchJson, postFile, postJson } from "@/lib/api";

type Doc = { id: number; filename: string; created_at: string; content_preview: string };
type TaskStatus = "open" | "in_progress" | "done";
type Task = {
  id: number;
  analysis_id: number;
  title: string;
  owner: string;
  priority: string;
  due_in_days: number;
  status: TaskStatus;
};
type Finding = { id: number; title: string; severity: string; evidence: string; recommendation: string };

type Health = { status: string; service: string };

type AnalysisSummary = {
  analysis_id: number;
  coverage_percent: number;
  risk_score: number;
  summary: string;
  findings_count: number;
  tasks_count: number;
  report_path: string;
};

type AnalysisDetails = {
  analysis: {
    id: number;
    framework: string;
    summary: string;
    coverage_percent: number;
    risk_score: number;
    created_at: string;
  };
  findings: Finding[];
  tasks: Task[];
};

export default function DashboardPage() {
  const [health, setHealth] = useState<Health | null>(null);
  const [documents, setDocuments] = useState<Doc[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [taskSearch, setTaskSearch] = useState("");
  const [taskStatusFilter, setTaskStatusFilter] = useState<"all" | TaskStatus>("open");
  const [taskPriorityFilter, setTaskPriorityFilter] = useState<"all" | "P1" | "P2" | "P3">("all");
  const [taskUpdatingId, setTaskUpdatingId] = useState<number | null>(null);
  const [selectedDocIds, setSelectedDocIds] = useState<number[]>([]);
  const [analysisSummary, setAnalysisSummary] = useState<AnalysisSummary | null>(null);
  const [analysisDetails, setAnalysisDetails] = useState<AnalysisDetails | null>(null);
  const [reportContent, setReportContent] = useState<string>("");
  const [copied, setCopied] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const openTasks = useMemo(() => tasks.filter((task) => task.status === "open").length, [tasks]);
  const reportContentUrl = analysisSummary
    ? `${API_BASE_URL}/api/v1/reports/${analysisSummary.analysis_id}/content`
    : "";
  const filteredTasks = useMemo(() => {
    const query = taskSearch.trim().toLowerCase();
    return tasks.filter((task) => {
      if (taskStatusFilter !== "all" && task.status !== taskStatusFilter) return false;
      if (taskPriorityFilter !== "all" && task.priority !== taskPriorityFilter) return false;
      if (!query) return true;
      return task.title.toLowerCase().includes(query) || String(task.analysis_id).includes(query);
    });
  }, [tasks, taskPriorityFilter, taskSearch, taskStatusFilter]);

  const loadDashboard = async () => {
    const [h, docs, taskItems] = await Promise.all([
      fetchJson<Health>("/health"),
      fetchJson<Doc[]>("/api/v1/documents"),
      fetchJson<Task[]>("/api/v1/tasks")
    ]);
    setHealth(h);
    setDocuments(docs);
    setTasks(taskItems);
  };

  useEffect(() => {
    loadDashboard().catch((err) => setError((err as Error).message));
  }, []);

  const refreshActiveAnalysis = async (analysisId: number) => {
    const details = await fetchJson<AnalysisDetails>(`/api/v1/analysis/${analysisId}`);
    setAnalysisDetails(details);
    const report = await fetchText(`/api/v1/reports/${analysisId}/content`);
    setReportContent(report);
  };

  const toggleDoc = (id: number) => {
    setSelectedDocIds((prev) => (prev.includes(id) ? prev.filter((v) => v !== id) : [...prev, id]));
  };

  const onUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files?.length) return;
    const file = event.target.files[0];
    setUploading(true);
    setError(null);
    try {
      await postFile("/api/v1/documents/upload", file);
      await loadDashboard();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  const runAnalysis = async () => {
    if (!selectedDocIds.length) {
      setError("Select at least one document before analysis.");
      return;
    }

    setAnalyzing(true);
    setError(null);

    try {
      const summary = await postJson<AnalysisSummary>("/api/v1/analysis/run", {
        document_ids: selectedDocIds,
        framework: "SME-BASELINE"
      });
      setAnalysisSummary(summary);
      await refreshActiveAnalysis(summary.analysis_id);
      setCopied(false);

      await loadDashboard();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setAnalyzing(false);
    }
  };

  const copyReport = async () => {
    if (!reportContent) return;
    try {
      await navigator.clipboard.writeText(reportContent);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      setError("Could not copy report to clipboard.");
    }
  };

  const updateTaskStatus = async (taskId: number, status: TaskStatus) => {
    setTaskUpdatingId(taskId);
    setError(null);
    try {
      await patchJson<Task>(`/api/v1/tasks/${taskId}`, { status });
      await loadDashboard();
      if (analysisSummary) {
        await refreshActiveAnalysis(analysisSummary.analysis_id);
      }
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setTaskUpdatingId(null);
    }
  };

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-6 py-10">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-slate-500">CompliQ Workspace</p>
          <h1 className="mt-2 font-[var(--font-display)] text-4xl font-bold text-ink">Compliance Dashboard</h1>
          <p className="mt-3 text-slate-700">Upload policy docs, run analysis, and generate remediation plans.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <a
            href="#all-open-tasks"
            className="rounded-xl bg-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            Manage Open Tasks
          </a>
          <a href="/" className="rounded-xl border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-500">
            Back To Landing
          </a>
        </div>
      </header>

      <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Service" value={health?.status === "ok" ? "Healthy" : "Pending"} helper={health?.service ?? "Waiting for backend"} />
        <StatCard label="Documents" value={String(documents.length)} helper="Uploaded for analysis" />
        <StatCard label="Open Tasks" value={String(openTasks)} helper="Pending remediation work (count only)" />
        <StatCard label="API Base" value="Connected" helper={API_BASE_URL} />
      </section>

      {error && (
        <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      <section className="mt-8 grid gap-6 xl:grid-cols-[1fr_1.2fr]">
        <SectionCard title="1) Upload & Select Documents">
          <div className="space-y-4">
            <label className="block rounded-xl border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-700">
              <span className="font-semibold text-ink">Upload document</span>
              <input type="file" className="mt-2 block w-full text-sm" onChange={onUpload} disabled={uploading} />
            </label>

            <div className="space-y-2">
              {documents.length === 0 ? (
                <p>No documents yet. Upload a policy file to begin.</p>
              ) : (
                documents.map((doc) => (
                  <label key={doc.id} className="flex cursor-pointer items-start gap-3 rounded-xl border border-slate-200 p-3">
                    <input type="checkbox" checked={selectedDocIds.includes(doc.id)} onChange={() => toggleDoc(doc.id)} className="mt-1" />
                    <div>
                      <p className="font-semibold text-ink">{doc.filename}</p>
                      <p className="text-xs text-slate-500">ID: {doc.id} • {new Date(doc.created_at).toLocaleString()}</p>
                      <p className="mt-1 text-xs text-slate-600">{doc.content_preview}</p>
                    </div>
                  </label>
                ))
              )}
            </div>

            <button
              onClick={runAnalysis}
              disabled={analyzing || uploading}
              className="rounded-xl bg-ink px-5 py-2 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {analyzing ? "Running analysis..." : "2) Run Compliance Analysis"}
            </button>
          </div>
        </SectionCard>

        <SectionCard title="3) Analysis Output">
          {!analysisSummary ? (
            <p>Run analysis to view findings, tasks, and report output.</p>
          ) : (
            <div className="space-y-4">
              <div className="grid gap-3 sm:grid-cols-3">
                <div className="rounded-xl bg-slate-50 p-3">
                  <p className="text-xs uppercase tracking-[0.12em] text-slate-500">Coverage</p>
                  <p className="text-xl font-bold text-ink">{analysisSummary.coverage_percent}%</p>
                </div>
                <div className="rounded-xl bg-slate-50 p-3">
                  <p className="text-xs uppercase tracking-[0.12em] text-slate-500">Risk Score</p>
                  <p className="text-xl font-bold text-ink">{analysisSummary.risk_score}/100</p>
                </div>
                <div className="rounded-xl bg-slate-50 p-3">
                  <p className="text-xs uppercase tracking-[0.12em] text-slate-500">Analysis ID</p>
                  <p className="text-xl font-bold text-ink">{analysisSummary.analysis_id}</p>
                </div>
              </div>

              <p className="rounded-xl border border-slate-200 p-3 text-sm text-slate-700">{analysisSummary.summary}</p>

              {analysisDetails?.findings?.length ? (
                <div>
                  <h4 className="font-semibold text-ink">Findings</h4>
                  <ul className="mt-2 space-y-2">
                    {analysisDetails.findings.map((f) => (
                      <li key={f.id} className="rounded-xl border border-slate-200 p-3">
                        <p className="font-semibold text-ink">{f.title}</p>
                        <p className="text-xs uppercase tracking-[0.12em] text-slate-500">{f.severity}</p>
                        <p className="mt-1 text-xs text-slate-700">Evidence: {f.evidence}</p>
                        <p className="mt-1 text-xs text-slate-700">Fix: {f.recommendation}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {analysisDetails?.tasks?.length ? (
                <div>
                  <h4 className="font-semibold text-ink">Tasks</h4>
                  <ul className="mt-2 space-y-2">
                    {analysisDetails.tasks.map((t) => (
                      <li key={t.id} className="rounded-xl border border-slate-200 p-3 text-sm">
                        <span className="font-semibold text-ink">{t.title}</span>
                        <span className="ml-2 text-xs text-slate-500">{t.priority} • {t.status}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {reportContent ? (
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h4 className="font-semibold text-ink">Report Content</h4>
                    <a
                      href={reportContentUrl}
                      target="_blank"
                      rel="noreferrer"
                      className="rounded-lg border border-slate-300 px-3 py-1 text-xs font-semibold text-slate-700 transition hover:border-slate-500"
                    >
                      Open Report
                    </a>
                    <button
                      onClick={copyReport}
                      className="rounded-lg border border-slate-300 px-3 py-1 text-xs font-semibold text-slate-700 transition hover:border-slate-500"
                    >
                      {copied ? "Copied" : "Copy Report"}
                    </button>
                  </div>
                  <pre className="mt-2 max-h-80 overflow-auto rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs text-slate-700">
                    {reportContent}
                  </pre>
                </div>
              ) : null}
            </div>
          )}
        </SectionCard>
      </section>

      <section id="all-open-tasks" className="mt-8">
        <SectionCard title="4) All Open Tasks Manager">
          <div className="space-y-4">
            <div className="grid gap-3 md:grid-cols-[2fr_1fr_1fr]">
              <input
                value={taskSearch}
                onChange={(event) => setTaskSearch(event.target.value)}
                placeholder="Search by task title or analysis ID..."
                className="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 outline-none ring-0 focus:border-slate-500"
              />
              <select
                value={taskStatusFilter}
                onChange={(event) => setTaskStatusFilter(event.target.value as "all" | TaskStatus)}
                className="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 outline-none ring-0 focus:border-slate-500"
              >
                <option value="all">All Status</option>
                <option value="open">Open</option>
                <option value="in_progress">In Progress</option>
                <option value="done">Done</option>
              </select>
              <select
                value={taskPriorityFilter}
                onChange={(event) => setTaskPriorityFilter(event.target.value as "all" | "P1" | "P2" | "P3")}
                className="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 outline-none ring-0 focus:border-slate-500"
              >
                <option value="all">All Priority</option>
                <option value="P1">P1</option>
                <option value="P2">P2</option>
                <option value="P3">P3</option>
              </select>
            </div>

            <p className="text-xs uppercase tracking-[0.12em] text-slate-500">
              Showing {filteredTasks.length} of {tasks.length} tasks
            </p>

            {filteredTasks.length === 0 ? (
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
                No tasks found for current filters.
              </div>
            ) : (
              <div className="space-y-2">
                {filteredTasks.map((task) => (
                  <div key={task.id} className="rounded-xl border border-slate-200 p-3">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div>
                        <p className="font-semibold text-ink">{task.title}</p>
                        <p className="mt-1 text-xs text-slate-500">
                          Task #{task.id} • Analysis #{task.analysis_id} • Owner: {task.owner} • Due in {task.due_in_days} days
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`rounded-full px-2 py-1 text-xs font-semibold ${
                            task.priority === "P1" ? "bg-red-100 text-red-700" : task.priority === "P2" ? "bg-amber-100 text-amber-700" : "bg-emerald-100 text-emerald-700"
                          }`}
                        >
                          {task.priority}
                        </span>
                        <span
                          className={`rounded-full px-2 py-1 text-xs font-semibold ${
                            task.status === "open"
                              ? "bg-slate-100 text-slate-700"
                              : task.status === "in_progress"
                                ? "bg-blue-100 text-blue-700"
                                : "bg-emerald-100 text-emerald-700"
                          }`}
                        >
                          {task.status === "in_progress" ? "in progress" : task.status}
                        </span>
                      </div>
                    </div>

                    <div className="mt-3 flex flex-wrap gap-2">
                      <button
                        onClick={() => updateTaskStatus(task.id, "open")}
                        disabled={task.status === "open" || taskUpdatingId === task.id}
                        className="rounded-lg border border-slate-300 px-3 py-1 text-xs font-semibold text-slate-700 transition hover:border-slate-500 disabled:cursor-not-allowed disabled:opacity-50"
                      >
                        Mark Open
                      </button>
                      <button
                        onClick={() => updateTaskStatus(task.id, "in_progress")}
                        disabled={task.status === "in_progress" || taskUpdatingId === task.id}
                        className="rounded-lg border border-slate-300 px-3 py-1 text-xs font-semibold text-slate-700 transition hover:border-slate-500 disabled:cursor-not-allowed disabled:opacity-50"
                      >
                        Mark In Progress
                      </button>
                      <button
                        onClick={() => updateTaskStatus(task.id, "done")}
                        disabled={task.status === "done" || taskUpdatingId === task.id}
                        className="rounded-lg border border-slate-300 px-3 py-1 text-xs font-semibold text-slate-700 transition hover:border-slate-500 disabled:cursor-not-allowed disabled:opacity-50"
                      >
                        Mark Done
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </SectionCard>
      </section>
    </main>
  );
}
