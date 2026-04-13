"use client";

import { useEffect, useState } from "react";

import { SectionCard } from "@/components/section-card";
import { StatCard } from "@/components/stat-card";
import { API_BASE_URL, fetchJson } from "@/lib/api";

type Doc = { id: number; filename: string; created_at: string };
type Task = { id: number; title: string; priority: string; status: string };

type Health = { status: string; service: string };

export default function DashboardPage() {
  const [health, setHealth] = useState<Health | null>(null);
  const [documents, setDocuments] = useState<Doc[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [h, docs, taskItems] = await Promise.all([
          fetchJson<Health>("/health"),
          fetchJson<Doc[]>("/api/v1/documents"),
          fetchJson<Task[]>("/api/v1/tasks")
        ]);
        setHealth(h);
        setDocuments(docs);
        setTasks(taskItems);
      } catch (err) {
        setError((err as Error).message);
      }
    };

    load();
  }, []);

  const openTasks = tasks.filter((task) => task.status === "open").length;

  return (
    <main className="mx-auto min-h-screen max-w-6xl px-6 py-10">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-slate-500">CompliQ Workspace</p>
          <h1 className="mt-2 font-[var(--font-display)] text-4xl font-bold text-ink">Compliance Dashboard</h1>
          <p className="mt-3 text-slate-700">Track uploaded documents, analysis status, remediation tasks, and backend health.</p>
        </div>
        <a href="/" className="rounded-xl border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-500">
          Back To Landing
        </a>
      </header>

      <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Service" value={health?.status === "ok" ? "Healthy" : "Pending"} helper={health?.service ?? "Waiting for backend"} />
        <StatCard label="Documents" value={String(documents.length)} helper="Uploaded for analysis" />
        <StatCard label="Open Tasks" value={String(openTasks)} helper="Pending remediation work" />
        <StatCard label="API Base" value="Connected" helper={API_BASE_URL} />
      </section>

      {error && (
        <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          Failed to load one or more API resources: {error}
        </div>
      )}

      <section className="mt-8 grid gap-6 lg:grid-cols-2">
        <SectionCard title="Recent Documents">
          {documents.length === 0 ? (
            <p>No documents yet. Use backend upload API to start your first analysis.</p>
          ) : (
            <ul className="space-y-3">
              {documents.slice(0, 6).map((doc) => (
                <li key={doc.id} className="rounded-xl border border-slate-200 p-3">
                  <p className="font-semibold text-ink">{doc.filename}</p>
                  <p className="text-xs text-slate-500">ID: {doc.id} • {new Date(doc.created_at).toLocaleString()}</p>
                </li>
              ))}
            </ul>
          )}
        </SectionCard>

        <SectionCard title="Action Queue">
          {tasks.length === 0 ? (
            <p>No tasks yet. Run an analysis to generate compliance remediation tasks.</p>
          ) : (
            <ul className="space-y-3">
              {tasks.slice(0, 8).map((task) => (
                <li key={task.id} className="rounded-xl border border-slate-200 p-3">
                  <p className="font-semibold text-ink">{task.title}</p>
                  <p className="text-xs text-slate-500">Priority: {task.priority} • Status: {task.status}</p>
                </li>
              ))}
            </ul>
          )}
        </SectionCard>
      </section>
    </main>
  );
}
