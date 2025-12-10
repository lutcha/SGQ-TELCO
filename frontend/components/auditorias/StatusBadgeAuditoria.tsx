import clsx from "clsx";
import { AuditoriaStatus } from "../../types/auditorias";

const STATUS_COLORS: Record<AuditoriaStatus, string> = {
  PLANEADA: "bg-slate-200 text-slate-800",
  PREPARACAO: "bg-amber-100 text-amber-800",
  EM_EXECUCAO: "bg-blue-100 text-blue-800",
  RELATORIO: "bg-indigo-100 text-indigo-800",
  CONCLUIDA: "bg-emerald-100 text-emerald-800",
  CANCELADA: "bg-rose-100 text-rose-800"
};

export function StatusBadgeAuditoria({ status }: { status: AuditoriaStatus }) {
  return (
    <span className={clsx("px-3 py-1 rounded-full text-xs font-semibold", STATUS_COLORS[status])}>
      {status.replace("_", " ")}
    </span>
  );
}
