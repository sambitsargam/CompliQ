interface StatCardProps {
  label: string;
  value: string;
  helper: string;
}

export function StatCard({ label, value, helper }: StatCardProps) {
  return (
    <div className="rounded-2xl border border-slate-200/70 bg-white/80 p-5 shadow-soft backdrop-blur">
      <p className="text-xs uppercase tracking-[0.18em] text-slate-500">{label}</p>
      <p className="mt-3 text-3xl font-semibold text-ink">{value}</p>
      <p className="mt-2 text-sm text-slate-600">{helper}</p>
    </div>
  );
}
