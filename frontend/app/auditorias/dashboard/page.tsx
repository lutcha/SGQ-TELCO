"use client";

import { useEffect, useState } from "react";
import { AuditoriaApi } from "../../../lib/api";
import { PageHeader } from "../../../components/common/PageHeader";
import { DashboardKpiCard } from "../../../components/auditorias/DashboardKpiCard";

export default function AuditoriaDashboardPage() {
  const [dashboard, setDashboard] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      const data = await AuditoriaApi.obterDashboard();
      setDashboard(data);
      setLoading(false);
    }
    load();
  }, []);

  if (loading) {
    return (
      <main className="max-w-6xl mx-auto px-6 py-10">
        <p className="text-sm text-slate-500">A carregar dashboard...</p>
      </main>
    );
  }

  return (
    <main className="max-w-6xl mx-auto px-6 py-10 space-y-8">
      <PageHeader title="Dashboard de Auditorias" description="KPIs e tendências" />

      <section className="grid md:grid-cols-4 gap-4">
        {dashboard?.kpis &&
          Object.entries(dashboard.kpis)
            .slice(0, 4)
            .map(([kpi, valor]) => <DashboardKpiCard key={kpi} label={kpi} value={String(valor)} />)}
      </section>

      <section className="grid md:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
          <h3 className="text-sm font-semibold text-slate-600 mb-2">Auditorias por Status</h3>
          <ul className="space-y-2 text-sm">
            {Object.entries(dashboard?.auditorias_por_status ?? {}).map(([status, total]) => (
              <li key={status} className="flex justify-between">
                <span>{status}</span>
                <span className="font-semibold">{total as number}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
          <h3 className="text-sm font-semibold text-slate-600 mb-2">Top Processos com NC</h3>
          <ul className="space-y-2 text-sm">
            {(dashboard?.kpis?.top_processos_nc ?? []).map((processo: any) => (
              <li key={processo.processo__id} className="flex justify-between">
                <span>{processo.processo_nome ?? processo.processo__nome}</span>
                <span className="font-semibold">{processo.total}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
        <h3 className="text-sm font-semibold text-slate-600 mb-3">Seguimento das Ações</h3>
        <ul className="space-y-2 text-sm">
          {Object.entries(dashboard?.seguimento?.por_status ?? {}).map(([status, total]) => (
            <li key={status} className="flex justify-between">
              <span>{status}</span>
              <span className="font-semibold">{total as number}</span>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
