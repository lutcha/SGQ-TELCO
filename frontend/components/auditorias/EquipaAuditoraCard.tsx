interface AuditorResumo {
  id: number;
  nome?: string;
  email?: string;
}

interface Props {
  lider?: AuditorResumo;
  auditores: AuditorResumo[];
}

export function EquipaAuditoraCard({ lider, auditores }: Props) {
  return (
    <div className="border border-slate-200 rounded-lg p-4 bg-white shadow-sm">
      <h3 className="text-sm font-semibold text-slate-600 mb-3">Equipa Auditora</h3>
      {lider && (
        <div className="mb-2">
          <p className="text-xs text-slate-500">Auditor Líder</p>
          <p className="font-medium">{lider.nome ?? `#${lider.id}`}</p>
        </div>
      )}
      <div>
        <p className="text-xs text-slate-500">Auditores</p>
        <ul className="mt-1 space-y-1">
          {auditores.length === 0 && <li className="text-sm text-slate-400">Sem auditores atribuídos</li>}
          {auditores.map((auditor) => (
            <li key={auditor.id} className="text-sm">
              {auditor.nome ?? `#${auditor.id}`}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
