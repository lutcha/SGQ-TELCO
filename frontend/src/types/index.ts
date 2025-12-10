// Types para o módulo de auditorias

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Tenant {
  id: number;
  nome: string;
  codigo: string;
  ativo: boolean;
  criado_em: string;
  atualizado_em: string;
}

export interface TipoAuditoria {
  id: number;
  nome: string;
  descricao: string;
  cor: string;
  ativo: boolean;
  criado_em: string;
  atualizado_em: string;
}

export interface Processo {
  id: number;
  codigo: string;
  nome: string;
  descricao: string;
  responsavel: number;
  responsavel_detalhes?: User;
  ativo: boolean;
  criado_em: string;
  atualizado_em: string;
}

export type StatusAuditoria = 'planejada' | 'em_andamento' | 'concluida' | 'cancelada';

export interface Auditoria {
  id: number;
  codigo: string;
  titulo: string;
  tipo: number;
  tipo_detalhes?: TipoAuditoria;
  descricao: string;
  objetivo: string;
  escopo: string;
  data_planejada_inicio: string;
  data_planejada_fim: string;
  data_real_inicio: string | null;
  data_real_fim: string | null;
  processos: number[];
  processos_detalhes?: Processo[];
  auditor_lider: number;
  auditor_lider_detalhes?: User;
  equipe_auditores: number[];
  equipe_auditores_detalhes?: User[];
  status: StatusAuditoria;
  status_display?: string;
  norma_referencia: string;
  criterios_auditoria: string;
  total_constatacoes?: number;
  constatacoes_abertas?: number;
  constatacoes_fechadas?: number;
  total_processos?: number;
  criado_por: number;
  criado_por_detalhes?: User;
  criado_em: string;
  atualizado_em: string;
}

export interface TipoConstatacao {
  id: number;
  nome: string;
  descricao: string;
  severidade: 1 | 2 | 3 | 4;
  severidade_display?: string;
  cor: string;
  requer_acao: boolean;
  ativo: boolean;
  criado_em: string;
  atualizado_em: string;
}

export type StatusConstatacao = 'aberta' | 'em_tratamento' | 'aguardando_validacao' | 'fechada' | 'cancelada';

export interface Constatacao {
  id: number;
  numero: string;
  auditoria: number;
  tipo: number;
  tipo_detalhes?: TipoConstatacao;
  processo: number;
  processo_detalhes?: Processo;
  titulo: string;
  descricao: string;
  evidencia: string;
  requisito: string;
  responsavel: number;
  responsavel_detalhes?: User;
  prazo_resposta: string;
  data_fechamento: string | null;
  status: StatusConstatacao;
  status_display?: string;
  analise_causa_raiz: string;
  dias_em_aberto?: number;
  total_acoes?: number;
  criado_por: number;
  criado_por_detalhes?: User;
  criado_em: string;
  atualizado_em: string;
}

export type TipoAcao = 'imediata' | 'corretiva' | 'preventiva';
export type StatusAcao = 'planejada' | 'em_andamento' | 'concluida' | 'verificada' | 'cancelada';

export interface AcaoCorretiva {
  id: number;
  numero: string;
  constatacao: number;
  tipo: TipoAcao;
  tipo_display?: string;
  descricao: string;
  objetivo: string;
  responsavel: number;
  responsavel_detalhes?: User;
  prazo_conclusao: string;
  data_conclusao: string | null;
  status: StatusAcao;
  status_display?: string;
  evidencia_execucao: string;
  verificada_por: number | null;
  verificada_por_detalhes?: User;
  data_verificacao: string | null;
  resultado_verificacao: string;
  eficaz: boolean | null;
  criado_por: number;
  criado_por_detalhes?: User;
  criado_em: string;
  atualizado_em: string;
}

export interface Comentario {
  id: number;
  auditoria: number | null;
  constatacao: number | null;
  texto: string;
  autor: number;
  autor_detalhes?: User;
  criado_em: string;
  atualizado_em: string;
}

export interface DocumentoAuditoria {
  id: number;
  auditoria: number;
  constatacao: number | null;
  tipo: 'plano' | 'checklist' | 'evidencia' | 'relatorio' | 'outro';
  tipo_display?: string;
  nome: string;
  descricao: string;
  arquivo: string;
  tamanho: number;
  enviado_por: number;
  enviado_por_detalhes?: User;
  enviado_em: string;
}

export interface Estatisticas {
  total_auditorias: number;
  auditorias_planejadas: number;
  auditorias_em_andamento: number;
  auditorias_concluidas: number;
  total_constatacoes: number;
  constatacoes_abertas: number;
  constatacoes_fechadas: number;
  taxa_fechamento: number;
  constatacoes_criticas: number;
  constatacoes_altas: number;
  acoes_atrasadas: number;
}

export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  detail?: string;
  message?: string;
  [key: string]: any;
}
