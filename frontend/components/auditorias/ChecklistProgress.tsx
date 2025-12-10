interface Props {
  total: number;
  concluido: number;
  naoConforme: number;
}

export function ChecklistProgress({ total, concluido, naoConforme }: Props) {
  const percent = total ? Math.round((concluido / total) * 100) : 0;
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-xs text-slate-500">
        <span>Checklist</span>
        <span>{percent}%</span>
      </div>
      <div className="h-2 rounded-full bg-slate-200 overflow-hidden">
        <div className="h-full bg-emerald-500" style={{ width: `${percent}%` }} />
      </div>
      <div className="text-xs text-slate-500">
        <span className="mr-3">Total: {total}</span>
        <span className="mr-3 text-emerald-600">Conforme: {concluido}</span>
        <span className="text-rose-600">NC: {naoConforme}</span>
      </div>
    </div>
  );
}
