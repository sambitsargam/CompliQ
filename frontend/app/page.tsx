import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="min-h-screen">
      <section className="grid-dots">
        <div className="mx-auto max-w-6xl px-6 pb-20 pt-16 md:pt-24">
          <nav className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-ink text-center text-lg font-bold leading-10 text-white">Q</div>
              <div>
                <p className="font-[var(--font-display)] text-xl font-bold text-ink">CompliQ</p>
                <p className="text-xs uppercase tracking-[0.18em] text-slate-500">Fast compliance, less stress</p>
              </div>
            </div>
            <Link href="/dashboard" className="rounded-full bg-ink px-5 py-2 text-sm font-semibold text-white transition hover:bg-slate-800">
              Open Dashboard
            </Link>
          </nav>

          <div className="mt-16 grid gap-10 md:grid-cols-[1.2fr_1fr] md:items-center">
            <div>
              <p className="inline-block rounded-full border border-mint/40 bg-mint/10 px-4 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-ink">
                Compliance Copilot For SMEs
              </p>
              <h1 className="mt-6 font-[var(--font-display)] text-4xl font-bold leading-tight text-ink md:text-6xl">
                Turn policy chaos into
                <span className="block text-mint">audit-ready clarity</span>
              </h1>
              <p className="mt-6 max-w-2xl text-lg text-slate-700">
                Upload your policy and process documents. CompliQ identifies control gaps, prioritizes risk,
                and gives your team a practical action plan with due dates and ownership.
              </p>

              <div className="mt-8 flex flex-wrap gap-4">
                <Link href="/dashboard" className="rounded-xl bg-ink px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">
                  Start Analysis
                </Link>
                <a href="#features" className="rounded-xl border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-500">
                  Explore Features
                </a>
              </div>
            </div>

            <div className="rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-soft">
              <h2 className="text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">Live Output Snapshot</h2>
              <div className="mt-5 space-y-4">
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs uppercase tracking-[0.12em] text-slate-500">Compliance Coverage</p>
                  <p className="mt-2 text-3xl font-bold text-ink">72%</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs uppercase tracking-[0.12em] text-slate-500">Risk Score</p>
                  <p className="mt-2 text-3xl font-bold text-ink">64 / 100</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-4 text-sm text-slate-700">
                  3 critical gaps found: ownership policy, incident escalation path, retention lifecycle.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="mx-auto max-w-6xl px-6 pb-24">
        <div className="grid gap-6 md:grid-cols-3">
          {[
            ["Evidence Mapping", "Extract obligations and map them to compliance controls."],
            ["Risk Prioritization", "Auto-score findings and rank remediation by urgency."],
            ["Actionable Plans", "Generate owner-based tasks with due windows and priorities."]
          ].map(([title, desc]) => (
            <article key={title} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft">
              <h3 className="font-[var(--font-display)] text-xl font-semibold text-ink">{title}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-700">{desc}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
