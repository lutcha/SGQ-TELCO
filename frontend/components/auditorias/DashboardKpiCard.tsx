interface Props {
  label: string;
  value: string | number;
  trend?: string;
}

export function DashboardKpiCard({ label, value, trend }: Props) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
      <p className="text-xs uppercase tracking-widest text-slate-400">{label}</p>
      <p className="text-2xl font-semibold text-slate-800 mt-2">{value}</p>
      {trend && <p className="text-xs text-emerald-600 mt-1">{trend}</p>}
    </div>
  );
}
