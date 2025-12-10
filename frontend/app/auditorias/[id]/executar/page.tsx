"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { AuditoriaApi } from "../../../../lib/api";
import { PageHeader } from "../../../../components/common/PageHeader";
import { StatusBadgeAuditoria } from "../../../../components/auditorias/StatusBadgeAuditoria";
import { ChecklistProgress } from "../../../../components/auditorias/ChecklistProgress";
import { ConstatacaoCard } from "../../../../components/auditorias/ConstatacaoCard";
import { EquipaAuditoraCard } from "../../../../components/auditorias/EquipaAuditoraCard";

interface AuditoriaDetalhe {
  id: number;
  numero_sequencial: string;
  status: any;
  ambito: string;
  auditor_lider?: any;
  auditores?: any[];
  checklists?: any[];
  constatacoes?: any[];
}

export default function ExecutarAuditoriaPage() {
  const params = useParams<{ id: string }>();
  const [auditoria, setAuditoria] = useState<AuditoriaDetalhe | null>(null);
  const [loading, setLoading] = useState(true);
  const [constatacaoTexto, setConstatacaoTexto] = useState("NC encontrada no requisito 8.2");

  const loadAuditoria = useCallback(async () => {
    if (!params?.id) return;
    setLoading(true);
    try {
      const data = await AuditoriaApi.obterAuditoria(Number(params.id));
      setAuditoria(data as any);
    } finally {
      setLoading(false);
    }
  }, [params?.id]);

  useEffect(() => {
    loadAuditoria();
  }, [loadAuditoria]);

  const criarConstatacao = useCallback(async () => {
    if (!params?.id) return;
    await AuditoriaApi.registarConstatacao(Number(params.id), {
      numero: `C-${Date.now()}`,
      tipo: "NAO_CONFORMIDADE",
      criticidade: "MAIOR",
      descricao: constatacaoTexto,
      evidencia: "Evidência registada",
      requisito_referencia: "ISO 9001 - 8.2",
      departamento_id: 1,
      identificada_por_id: 1
    });
    await loadAuditoria();
  }, [constatacaoTexto, loadAuditoria, params?.id]);

  if (loading) {
    return (
      <main className="max-w-5xl mx-auto px-6 py-10">
        <p className="text-sm text-slate-500">A carregar auditoria...</p>
      </main>
    );
  }

  if (!auditoria) {
    return (
      <main className="max-w-5xl mx-auto px-6 py-10">
        <p className="text-sm text-slate-500">Auditoria não encontrada.</p>
      </main>
    );
  }

  const checklists = auditoria.checklists ?? [];
  const constatacoes = auditoria.constatacoes ?? [];

  return (
    <main className="max-w-5xl mx-auto px-6 py-10 space-y-6">
      <PageHeader title={`Execução ${auditoria.numero_sequencial}`} description={auditoria.ambito} />
      <div className="flex items-center gap-4">
        <StatusBadgeAuditoria status={auditoria.status} />
        <button className="text-xs bg-sky-600 text-white px-3 py-1 rounded" onClick={() => AuditoriaApi.executarAcao(auditoria.id, "iniciar")}>Iniciar</button>
        <button className="text-xs bg-emerald-600 text-white px-3 py-1 rounded" onClick={() => AuditoriaApi.executarAcao(auditoria.id, "concluir")}>Concluir</button>
      </div>

      <section className="grid md:grid-cols-3 gap-4">
        <div className="md:col-span-2 space-y-4">
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-600 mb-4">Checklists</h3>
            {checklists.length === 0 && <p className="text-sm text-slate-500">Sem checklists atribuídos.</p>}
            {checklists.map((checklist) => (
              <div key={checklist.id} className="border border-slate-100 rounded-lg p-3 mb-3">
                <div className="flex justify-between items-center mb-2">
                  <p className="font-semibold text-slate-800">{checklist.titulo}</p>
                  <ChecklistProgress total={checklist.itens?.length ?? 0} concluido={checklist.itens?.filter((item: any) => item.status === "CONFORME").length ?? 0} naoConforme={checklist.itens?.filter((item: any) => item.status === "NAO_CONFORME").length ?? 0} />
                </div>
                <ul className="text-sm text-slate-600 space-y-2">
                  {checklist.itens?.slice(0, 3).map((item: any) => (
                    <li key={item.id} className="flex justify-between gap-4">
                      <span>{item.questao}</span>
                      <span className="text-xs text-slate-400">{item.status}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-slate-600">Constatações</h3>
              <button className="text-xs text-sky-600" onClick={criarConstatacao}>
                Registar
              </button>
            </div>
            <textarea className="w-full border border-slate-200 rounded-md px-3 py-2 text-sm mb-4" rows={3} value={constatacaoTexto} onChange={(event) => setConstatacaoTexto(event.target.value)} />
            <div className="grid gap-3">
              {constatacoes.map((constatacao) => (
                <ConstatacaoCard key={constatacao.id} constatacao={constatacao as any} />
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <EquipaAuditoraCard lider={auditoria.auditor_lider} auditores={auditoria.auditores ?? []} />
        </div>
      </section>
    </main>
  );
}
