"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { AuditoriaApi } from "../../../../lib/api";
import { PageHeader } from "../../../../components/common/PageHeader";
import { RelatorioPreview } from "../../../../components/auditorias/RelatorioPreview";

interface RelatorioForm {
  resumo_executivo: string;
  objetivos: string;
  metodologia: string;
  conclusoes: string;
}

const INITIAL_RELATORIO: RelatorioForm = {
  resumo_executivo: "",
  objetivos: "",
  metodologia: "",
  conclusoes: ""
};

export default function RelatorioAuditoriaPage() {
  const params = useParams<{ id: string }>();
  const [relatorio, setRelatorio] = useState<RelatorioForm>(INITIAL_RELATORIO);
  const [mensagem, setMensagem] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!params?.id) return;
    const data = await AuditoriaApi.obterAuditoria(Number(params.id));
    if ((data as any).relatorio) {
      setRelatorio({
        resumo_executivo: (data as any).relatorio.resumo_executivo,
        objetivos: (data as any).relatorio.objetivos,
        metodologia: (data as any).relatorio.metodologia,
        conclusoes: (data as any).relatorio.conclusoes
      });
    }
  }, [params?.id]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function guardar() {
    if (!params?.id) return;
    setMensagem(null);
    try {
      await AuditoriaApi.guardarRelatorio(Number(params.id), {
        ...relatorio,
        ambito_detalhado: "",
        sintese_resultados: "",
        total_constatacoes: 0,
        elaborado_por_id: 1,
        data_elaboracao: new Date().toISOString().slice(0, 10)
      });
      setMensagem("Relatório guardado. Pode gerar o PDF quando concluir.");
    } catch (err) {
      setMensagem((err as Error).message);
    }
  }

  async function gerarPdf() {
    if (!params?.id) return;
    await AuditoriaApi.gerarPdf(Number(params.id));
    setMensagem("PDF gerado (placeholder)");
  }

  return (
    <main className="max-w-4xl mx-auto px-6 py-10 space-y-6">
      <PageHeader title="Relatório da Auditoria" description="Edição estruturada" />

      <div className="grid md:grid-cols-2 gap-6">
        <form className="bg-white border border-slate-200 rounded-xl shadow-sm p-4 space-y-4" onSubmit={(event) => event.preventDefault()}>
          {Object.entries(relatorio).map(([campo, valor]) => (
            <div key={campo}>
              <label className="text-xs text-slate-500 capitalize">{campo.replace("_", " ")}</label>
              <textarea className="w-full border border-slate-200 rounded-md px-3 py-2 text-sm" rows={4} value={valor} onChange={(event) => setRelatorio((prev) => ({ ...prev, [campo]: event.target.value }))} />
            </div>
          ))}
          <div className="flex gap-3">
            <button type="button" className="bg-sky-600 text-white px-4 py-2 rounded-md text-sm" onClick={guardar}>
              Guardar
            </button>
            <button type="button" className="bg-emerald-600 text-white px-4 py-2 rounded-md text-sm" onClick={gerarPdf}>
              Gerar PDF
            </button>
          </div>
          {mensagem && <p className="text-xs text-slate-500">{mensagem}</p>}
        </form>
        <RelatorioPreview resumo={relatorio.resumo_executivo} conclusoes={relatorio.conclusoes} />
      </div>
    </main>
  );
}
