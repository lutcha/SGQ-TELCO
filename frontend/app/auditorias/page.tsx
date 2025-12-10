"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useAuditorias } from "../../hooks/useAuditorias";
import { StatusBadgeAuditoria } from "../../components/auditorias/StatusBadgeAuditoria";
import { TipoBadge } from "../../components/auditorias/TipoBadge";
import { PageHeader } from "../../components/common/PageHeader";
import { formatDate } from "../../utils/format";
import { AuditoriaStatus, AuditoriaTipo } from "../../types/auditorias";

const STATUS_OPTIONS: AuditoriaStatus[] = ["PLANEADA", "PREPARACAO", "EM_EXECUCAO", "RELATORIO", "CONCLUIDA", "CANCELADA"];
const TIPO_OPTIONS: AuditoriaTipo[] = ["INTERNA_GLOBAL", "INTERNA_PARCIAL", "EXTERNA", "FORNECEDOR"];

export default function AuditoriasPage() {
  const [filters, setFilters] = useState<Record<string, string>>({});
  const { data, isLoading, refetch } = useAuditorias(filters);
  const auditorias = useMemo(() => data ?? [], [data]);

  const totalPorStatus = useMemo(() => {
    return auditorias.reduce<Record<string, number>>((acc, auditoria) => {
      acc[auditoria.status] = (acc[auditoria.status] ?? 0) + 1;
      return acc;
    }, {});
  }, [auditorias]);

  return (
    <main className="max-w-6xl mx-auto px-6 py-10">
      <PageHeader
        title="Auditorias"
        description="Planeamento e execução das auditorias ISO 9001"
        actions={
          <Link href="/auditorias/nova" className="bg-sky-600 text-white px-4 py-2 rounded-md text-sm font-medium">
            Nova Auditoria
          </Link>
        }
      />

      <section className="grid grid-cols-2 md:grid-cols-6 gap-3 mb-6">
        {STATUS_OPTIONS.map((status) => (
          <div key={status} className="bg-white border border-slate-200 rounded-lg p-3 text-center">
            <p className="text-xs text-slate-500">{status}</p>
            <p className="text-2xl font-semibold text-slate-800">{totalPorStatus[status] ?? 0}</p>
          </div>
        ))}
      </section>

      <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
        <form
          className="grid md:grid-cols-5 gap-4 mb-6"
          onSubmit={(event) => {
            event.preventDefault();
            refetch();
          }}
        >
          <div>
            <label className="text-xs text-slate-500">Status</label>
            <select
              className="w-full border border-slate-200 rounded-md px-2 py-2"
              value={filters.status ?? ""}
              onChange={(event) => setFilters((prev) => ({ ...prev, status: event.target.value }))}
            >
              <option value="">Todos</option>
              {STATUS_OPTIONS.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs text-slate-500">Tipo</label>
            <select
              className="w-full border border-slate-200 rounded-md px-2 py-2"
              value={filters.tipo ?? ""}
              onChange={(event) => setFilters((prev) => ({ ...prev, tipo: event.target.value }))}
            >
              <option value="">Todos</option>
              {TIPO_OPTIONS.map((tipo) => (
                <option key={tipo} value={tipo}>
                  {tipo}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs text-slate-500">Ano</label>
            <input
              type="number"
              className="w-full border border-slate-200 rounded-md px-2 py-2"
              value={filters.ano ?? ""}
              onChange={(event) => setFilters((prev) => ({ ...prev, ano: event.target.value }))}
            />
          </div>
          <div className="md:col-span-2 flex items-end justify-end gap-3">
            <button type="button" className="text-sm text-slate-500" onClick={() => setFilters({})}>
              Limpar
            </button>
            <button type="submit" className="bg-slate-900 text-white px-4 py-2 rounded-md text-sm font-semibold">
              Aplicar
            </button>
          </div>
        </form>

        <div className="table-wrapper">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="text-xs text-slate-500">
                <th className="py-2">Número</th>
                <th>Tipo</th>
                <th>Status</th>
                <th>Período</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {isLoading && (
                <tr>
                  <td colSpan={5} className="text-center py-6 text-slate-400">
                    A carregar auditorias...
                  </td>
                </tr>
              )}
              {!isLoading && auditorias.length === 0 && (
                <tr>
                  <td colSpan={5} className="text-center py-6 text-slate-400">
                    Ainda não existem auditorias.
                  </td>
                </tr>
              )}
              {auditorias.map((auditoria) => (
                <tr key={auditoria.id} className="border-t border-slate-100">
                  <td className="py-3">
                    <p className="font-semibold text-slate-800">{auditoria.numero_sequencial}</p>
                    <p className="text-xs text-slate-500">{auditoria.ambito}</p>
                  </td>
                  <td>
                    <TipoBadge tipo={auditoria.tipo as AuditoriaTipo} />
                  </td>
                  <td>
                    <StatusBadgeAuditoria status={auditoria.status as AuditoriaStatus} />
                  </td>
                  <td>
                    <p className="text-xs text-slate-500">
                      {formatDate(auditoria.data_prevista_inicio)} → {formatDate(auditoria.data_prevista_fim)}
                    </p>
                  </td>
                  <td className="text-right">
                    <div className="flex gap-2 justify-end">
                      <Link className="text-xs text-sky-600" href={`/auditorias/${auditoria.id}/executar`}>
                        Executar
                      </Link>
                      <Link className="text-xs text-slate-500" href={`/auditorias/${auditoria.id}/relatorio`}>
                        Relatório
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
