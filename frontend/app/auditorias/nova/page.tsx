"use client";

import { FormEvent, useMemo, useState } from "react";
import { AuditoriaApi } from "../../../lib/api";
import { PageHeader } from "../../../components/common/PageHeader";

const STEPS = ["Dados Básicos", "Processos e Departamentos", "Equipa Auditora", "Revisão"];

interface FormState {
  numero_sequencial: string;
  tipo: string;
  ambito: string;
  data_prevista_inicio: string;
  data_prevista_fim: string;
  processos: string;
  departamentos: string;
  auditor_lider: string;
  auditores: string;
}

const INITIAL_STATE: FormState = {
  numero_sequencial: "AUD-",
  tipo: "INTERNA_GLOBAL",
  ambito: "",
  data_prevista_inicio: new Date().toISOString().slice(0, 10),
  data_prevista_fim: new Date().toISOString().slice(0, 10),
  processos: "",
  departamentos: "",
  auditor_lider: "",
  auditores: ""
};

export default function NovaAuditoriaPage() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<FormState>(INITIAL_STATE);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const preview = useMemo(
    () => `Auditoria ${form.numero_sequencial}\nTipo: ${form.tipo}\nPeríodo: ${form.data_prevista_inicio} → ${form.data_prevista_fim}`,
    [form]
  );

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (step < STEPS.length - 1) {
      setStep((prev) => prev + 1);
      return;
    }
    setSubmitting(true);
    setMessage(null);
    try {
      await AuditoriaApi.criarAuditoria({
        numero_sequencial: form.numero_sequencial,
        tipo: form.tipo as any,
        ambito: form.ambito,
        data_prevista_inicio: form.data_prevista_inicio,
        data_prevista_fim: form.data_prevista_fim,
        processos: form.processos.split(",").map((p) => Number(p.trim())).filter(Boolean),
        departamentos: form.departamentos.split(",").map((d) => Number(d.trim())).filter(Boolean),
        auditor_lider: Number(form.auditor_lider),
        auditores: form.auditores.split(",").map((id) => Number(id.trim())).filter(Boolean)
      } as any);
      setMessage("Auditoria criada com sucesso. Continue a preparação na lista principal.");
      setForm(INITIAL_STATE);
      setStep(0);
    } catch (err) {
      setMessage((err as Error).message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <PageHeader title="Nova Auditoria" description="Assistente passo a passo" />

      <ol className="flex gap-4 mb-8">
        {STEPS.map((label, index) => (
          <li key={label} className={`flex-1 text-center text-xs ${index === step ? "text-sky-600 font-semibold" : "text-slate-400"}`}>
            {index + 1}. {label}
          </li>
        ))}
      </ol>

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
        <form className="space-y-4" onSubmit={handleSubmit}>
          {step === 0 && (
            <>
              <div>
                <label className="text-xs text-slate-500">Número</label>
                <input
                  className="w-full border border-slate-200 rounded-md px-3 py-2"
                  value={form.numero_sequencial}
                  onChange={(event) => setForm((prev) => ({ ...prev, numero_sequencial: event.target.value }))}
                />
              </div>
              <div>
                <label className="text-xs text-slate-500">Tipo</label>
                <select
                  className="w-full border border-slate-200 rounded-md px-3 py-2"
                  value={form.tipo}
                  onChange={(event) => setForm((prev) => ({ ...prev, tipo: event.target.value }))}
                >
                  <option value="INTERNA_GLOBAL">Interna Global</option>
                  <option value="INTERNA_PARCIAL">Interna Parcial</option>
                  <option value="EXTERNA">Externa</option>
                  <option value="FORNECEDOR">Fornecedor</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-slate-500">Âmbito</label>
                <textarea
                  className="w-full border border-slate-200 rounded-md px-3 py-2"
                  rows={3}
                  value={form.ambito}
                  onChange={(event) => setForm((prev) => ({ ...prev, ambito: event.target.value }))}
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-xs text-slate-500">Data início</label>
                  <input
                    type="date"
                    className="w-full border border-slate-200 rounded-md px-3 py-2"
                    value={form.data_prevista_inicio}
                    onChange={(event) => setForm((prev) => ({ ...prev, data_prevista_inicio: event.target.value }))}
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-500">Data fim</label>
                  <input
                    type="date"
                    className="w-full border border-slate-200 rounded-md px-3 py-2"
                    value={form.data_prevista_fim}
                    onChange={(event) => setForm((prev) => ({ ...prev, data_prevista_fim: event.target.value }))}
                  />
                </div>
              </div>
            </>
          )}

          {step === 1 && (
            <>
              <div>
                <label className="text-xs text-slate-500">Processos (IDs separados por vírgula)</label>
                <input
                  className="w-full border border-slate-200 rounded-md px-3 py-2"
                  value={form.processos}
                  onChange={(event) => setForm((prev) => ({ ...prev, processos: event.target.value }))}
                />
              </div>
              <div>
                <label className="text-xs text-slate-500">Departamentos (IDs separados por vírgula)</label>
                <input
                  className="w-full border border-slate-200 rounded-md px-3 py-2"
                  value={form.departamentos}
                  onChange={(event) => setForm((prev) => ({ ...prev, departamentos: event.target.value }))}
                />
              </div>
            </>
          )}

          {step === 2 && (
            <>
              <div>
                <label className="text-xs text-slate-500">Auditor líder (ID)</label>
                <input
                  className="w-full border border-slate-200 rounded-md px-3 py-2"
                  value={form.auditor_lider}
                  onChange={(event) => setForm((prev) => ({ ...prev, auditor_lider: event.target.value }))}
                />
              </div>
              <div>
                <label className="text-xs text-slate-500">Auditores (IDs separados por vírgula)</label>
                <input
                  className="w-full border border-slate-200 rounded-md px-3 py-2"
                  value={form.auditores}
                  onChange={(event) => setForm((prev) => ({ ...prev, auditores: event.target.value }))}
                />
              </div>
            </>
          )}

          {step === 3 && (
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 text-sm whitespace-pre-line">
              {preview}
            </div>
          )}

          {message && <p className="text-sm text-slate-600">{message}</p>}

          <div className="flex justify-between">
            <button type="button" className="text-sm text-slate-500" disabled={step === 0} onClick={() => setStep((prev) => Math.max(prev - 1, 0))}>
              Voltar
            </button>
            <button type="submit" className="bg-sky-600 text-white px-4 py-2 rounded-md text-sm font-semibold" disabled={submitting}>
              {step === STEPS.length - 1 ? (submitting ? "A criar..." : "Finalizar") : "Avançar"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}
