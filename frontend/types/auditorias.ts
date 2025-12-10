export type ProgramaStatus = "RASCUNHO" | "APROVADO" | "EM_EXECUCAO" | "CONCLUIDO";
export type AuditoriaTipo = "INTERNA_GLOBAL" | "INTERNA_PARCIAL" | "EXTERNA" | "FORNECEDOR";
export type AuditoriaStatus = "PLANEADA" | "PREPARACAO" | "EM_EXECUCAO" | "RELATORIO" | "CONCLUIDA" | "CANCELADA";

export interface ProgramaAuditoria {
  id: number;
  ano: number;
  versao: string;
  data_elaboracao: string;
  data_aprovacao: string | null;
  elaborado_por: number | Record<string, unknown>;
  aprovado_por: number | Record<string, unknown> | null;
  status: ProgramaStatus;
  total_auditorias: number;
  auditorias_concluidas: number;
  observacoes: string;
}

export interface Auditoria {
  id: number;
  programa: number | ProgramaAuditoria;
  numero_sequencial: string;
  tipo: AuditoriaTipo;
  ambito: string;
  data_prevista_inicio: string;
  data_prevista_fim: string;
  data_real_inicio: string | null;
  data_real_fim: string | null;
  processos: number[];
  departamentos: number[];
  auditor_lider: number | Record<string, unknown>;
  auditores: number[];
  status: AuditoriaStatus;
  total_constatacoes: number;
  nao_conformidades_encontradas: number;
  oportunidades_melhoria: number;
}

export interface ChecklistItem {
  id: number;
  numero: string;
  requisito: string;
  questao: string;
  status: string;
  observacao: string;
  evidencia: string;
}

export interface Checklist {
  id: number;
  titulo: string;
  descricao: string;
  itens: ChecklistItem[];
}

export interface Constatacao {
  id: number;
  numero: string;
  tipo: string;
  criticidade: string | null;
  descricao: string;
  evidencia: string;
  departamento: { id: number; nome: string };
}

export interface AuditoriaDashboard {
  kpis: Record<string, unknown>;
  auditorias_por_status: Record<string, number>;
  timeline: Array<Record<string, unknown>>;
  mapa_calor: Array<Record<string, unknown>>;
  programa: Record<string, unknown>;
  constatacoes: Record<string, unknown>;
  seguimento: Record<string, unknown>;
}
