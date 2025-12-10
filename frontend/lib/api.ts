import { Auditoria, AuditoriaDashboard, ProgramaAuditoria } from "../types/auditorias";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

async function apiFetch<T>(endpoint: string, options?: { method?: HttpMethod; body?: unknown; params?: Record<string, unknown> }) {
  const url = new URL(`${API_BASE}${endpoint}`);
  if (options?.params) {
    Object.entries(options.params).forEach(([key, value]) => {
      if (value === undefined || value === null || value === "") return;
      url.searchParams.append(key, String(value));
    });
  }

  const response = await fetch(url.toString(), {
    method: options?.method ?? "GET",
    headers: {
      "Content-Type": "application/json"
    },
    cache: options?.method === "GET" ? "no-store" : "no-cache",
    body: options?.body ? JSON.stringify(options.body) : undefined
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Erro na API");
  }
  if (response.status === 204) {
    return null as T;
  }
  return (await response.json()) as T;
}

export const AuditoriaApi = {
  listarProgramas(params?: Record<string, unknown>) {
    return apiFetch<{ results: ProgramaAuditoria[] }>("/auditorias/programas/", { params });
  },
  criarPrograma(payload: Partial<ProgramaAuditoria>) {
    return apiFetch<ProgramaAuditoria>("/auditorias/programas/", { method: "POST", body: payload });
  },
  listarAuditorias(params?: Record<string, unknown>) {
    return apiFetch<{ results: Auditoria[] }>("/auditorias/", { params });
  },
  obterAuditoria(id: number) {
    return apiFetch<Auditoria>(`/auditorias/${id}/`);
  },
  criarAuditoria(payload: Partial<Auditoria>) {
    return apiFetch<Auditoria>("/auditorias/", { method: "POST", body: payload });
  },
  atualizarAuditoria(id: number, payload: Partial<Auditoria>) {
    return apiFetch<Auditoria>(`/auditorias/${id}/`, { method: "PUT", body: payload });
  },
  executarAcao(id: number, acao: "iniciar" | "concluir" | "cancelar") {
    return apiFetch(`/auditorias/${id}/${acao}/`, { method: "POST" });
  },
  obterDashboard() {
    return apiFetch<AuditoriaDashboard>("/auditorias/dashboard/");
  },
  obterStats() {
    return apiFetch<Record<string, unknown>>("/auditorias/stats/");
  },
  guardarChecklist(auditoriaId: number, payload: unknown) {
    return apiFetch(`/auditorias/${auditoriaId}/checklists/`, { method: "POST", body: payload });
  },
  registarConstatacao(auditoriaId: number, payload: unknown) {
    return apiFetch(`/auditorias/${auditoriaId}/constatacoes/`, { method: "POST", body: payload });
  },
  guardarRelatorio(auditoriaId: number, payload: unknown) {
    return apiFetch(`/auditorias/${auditoriaId}/relatorio/`, { method: "POST", body: payload });
  },
  atualizarRelatorio(auditoriaId: number, payload: unknown) {
    return apiFetch(`/auditorias/${auditoriaId}/relatorio/`, { method: "PUT", body: payload });
  },
  gerarPdf(auditoriaId: number) {
    return apiFetch(`/auditorias/${auditoriaId}/relatorio/gerar-pdf/`, { method: "POST" });
  }
};
