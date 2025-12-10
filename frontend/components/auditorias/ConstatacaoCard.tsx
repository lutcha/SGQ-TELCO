import { Constatacao } from "../../types/auditorias";
import clsx from "clsx";

const CRITICIDADE = {
  CRITICA: "bg-rose-100 text-rose-700",
  MAIOR: "bg-amber-100 text-amber-700",
  MENOR: "bg-emerald-100 text-emerald-700"
};

export function ConstatacaoCard({ constatacao }: { constatacao: Constatacao }) {
  return (
    <article className="border border-slate-200 rounded-lg p-4 bg-white shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-semibold text-slate-800">{constatacao.numero}</h4>
        {constatacao.criticidade && (
          <span className={clsx("px-2 py-0.5 rounded text-xs font-semibold", CRITICIDADE[constatacao.criticidade as keyof typeof CRITICIDADE])}>
            {constatacao.criticidade}
          </span>
        )}
      </div>
      <p className="text-sm text-slate-600 mb-2">{constatacao.descricao}</p>
      <p className="text-xs text-slate-500">Departamento: {constatacao.departamento?.nome}</p>
    </article>
  );
}
