"use client";

import { FormEvent, useEffect, useState } from "react";
import { AuditoriaApi } from "../../../lib/api";
import { ProgramaAuditoria } from "../../../types/auditorias";
import { PageHeader } from "../../../components/common/PageHeader";

export default function ProgramaAuditoriaPage() {
  const [programas, setProgramas] = useState<ProgramaAuditoria[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    ano: new Date().getFullYear().toString(),
    versao: "1",
    data_elaboracao: new Date().toISOString().slice(0, 10)
  });
  const [error, setError] = useState<string | null>(null);

  async function loadProgramas() {
    setLoading(true);
    try {
      const data = await AuditoriaApi.listarProgramas();
      setProgramas(data.results);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProgramas();
  }, []);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    try {
      await AuditoriaApi.criarPrograma({
        ano: Number(form.ano),
        versao: form.versao,
        data_elaboracao: form.data_elaboracao,
        observacoes: "",
        status: "RASCUNHO"
      });
      await loadProgramas();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <main className="max-w-5xl mx-auto px-6 py-10">
      <PageHeader title="Programa Anual" description="Planeamento macro e aprovação do programa" />

      {error && <p className="text-sm text-rose-600 mb-4">{error}</p>}

      <section className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm">
            <header className="px-4 py-3 border-b border-slate-100 flex justify-between">
              <h2 className="text-sm font-semibold text-slate-600">Programas</h2>
              <button onClick={loadProgramas} className="text-xs text-slate-500">
                Atualizar
              </button>
            </header>
            <div className="divide-y divide-slate-100">
              {loading && <p className="p-4 text-sm text-slate-500">A carregar...</p>}
              {!loading && programas.length === 0 && <p className="p-4 text-sm text-slate-500">Sem programas ainda.</p>}
              {programas.map((programa) => (
                <article key={programa.id} className="p-4">
                  <p className="text-sm font-semibold text-slate-800">
                    {programa.ano}/{programa.versao}
                  </p>
                  <p className="text-xs text-slate-500">Status: {programa.status}</p>
                  <p className="text-xs text-slate-500">Auditorias previstas: {programa.total_auditorias}</p>
                </article>
              ))}
            </div>
          </div>
        </div>
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-4">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Novo programa</h3>
          <form className="space-y-3" onSubmit={onSubmit}>
            <div>
              <label className="text-xs text-slate-500">Ano</label>
              <input
                className="w-full border border-slate-200 rounded-md px-2 py-2"
                value={form.ano}
                onChange={(event) => setForm((prev) => ({ ...prev, ano: event.target.value }))}
              />
            </div>
            <div>
              <label className="text-xs text-slate-500">Versão</label>
              <input
                className="w-full border border-slate-200 rounded-md px-2 py-2"
                value={form.versao}
                onChange={(event) => setForm((prev) => ({ ...prev, versao: event.target.value }))}
              />
            </div>
            <div>
              <label className="text-xs text-slate-500">Data elaboração</label>
              <input
                type="date"
                className="w-full border border-slate-200 rounded-md px-2 py-2"
                value={form.data_elaboracao}
                onChange={(event) => setForm((prev) => ({ ...prev, data_elaboracao: event.target.value }))}
              />
            </div>
            <button type="submit" className="w-full bg-sky-600 text-white py-2 rounded-md text-sm font-medium">
              Criar programa
            </button>
          </form>
        </div>
      </section>
    </main>
  );
}
