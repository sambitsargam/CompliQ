interface SectionCardProps {
  title: string;
  children: React.ReactNode;
}

export function SectionCard({ title, children }: SectionCardProps) {
  return (
    <section className="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-soft">
      <h3 className="text-lg font-semibold text-ink">{title}</h3>
      <div className="mt-4 text-sm text-slate-700">{children}</div>
    </section>
  );
}
