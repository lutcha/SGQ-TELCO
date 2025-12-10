import clsx from "clsx";
import { AuditoriaTipo } from "../../types/auditorias";

const TYPE_COLORS: Record<AuditoriaTipo, string> = {
  INTERNA_GLOBAL: "border-sky-600 text-sky-700",
  INTERNA_PARCIAL: "border-cyan-600 text-cyan-700",
  EXTERNA: "border-purple-600 text-purple-700",
  FORNECEDOR: "border-emerald-600 text-emerald-700"
};

export function TipoBadge({ tipo }: { tipo: AuditoriaTipo }) {
  return (
    <span className={clsx("px-2 py-0.5 text-xs font-medium border rounded-md", TYPE_COLORS[tipo])}>
      {tipo.replace("_", " ")}
    </span>
  );
}
