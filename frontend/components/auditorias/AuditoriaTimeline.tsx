interface EventoTimeline {
  titulo: string;
  dataPrevista: string;
  dataReal?: string | null;
  status: string;
}

export function AuditoriaTimeline({ eventos }: { eventos: EventoTimeline[] }) {
  return (
    <ol className="border-l border-slate-200 pl-4 space-y-4">
      {eventos.map((evento) => (
        <li key={evento.titulo} className="relative">
          <span className="absolute -left-5 top-1 w-2 h-2 rounded-full bg-sky-500" />
          <p className="text-sm font-semibold text-slate-700">{evento.titulo}</p>
          <p className="text-xs text-slate-500">
            Previsto: {evento.dataPrevista}
            {evento.dataReal && <span className="ml-2">Real: {evento.dataReal}</span>}
          </p>
          <p className="text-xs uppercase tracking-wide text-slate-400">{evento.status}</p>
        </li>
      ))}
    </ol>
  );
}
