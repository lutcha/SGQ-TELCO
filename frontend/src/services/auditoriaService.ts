import { api, PaginatedResponse } from '@/lib/api';
import {
  Auditoria,
  Constatacao,
  AcaoCorretiva,
  TipoAuditoria,
  TipoConstatacao,
  Processo,
  DocumentoAuditoria,
  Comentario,
  Estatisticas,
} from '@/types';

// Serviço de Auditorias
export const auditoriaService = {
  // Listar auditorias
  list: async (params?: any) => {
    const { data } = await api.get<PaginatedResponse<Auditoria>>('/auditorias/auditorias/', { params });
    return data;
  },

  // Obter auditoria por ID
  get: async (id: number) => {
    const { data } = await api.get<Auditoria>(`/auditorias/auditorias/${id}/`);
    return data;
  },

  // Criar auditoria
  create: async (auditoria: Partial<Auditoria>) => {
    const { data } = await api.post<Auditoria>('/auditorias/auditorias/', auditoria);
    return data;
  },

  // Atualizar auditoria
  update: async (id: number, auditoria: Partial<Auditoria>) => {
    const { data } = await api.patch<Auditoria>(`/auditorias/auditorias/${id}/`, auditoria);
    return data;
  },

  // Deletar auditoria
  delete: async (id: number) => {
    await api.delete(`/auditorias/auditorias/${id}/`);
  },

  // Iniciar auditoria
  iniciar: async (id: number) => {
    const { data } = await api.post<Auditoria>(`/auditorias/auditorias/${id}/iniciar/`);
    return data;
  },

  // Concluir auditoria
  concluir: async (id: number) => {
    const { data } = await api.post<Auditoria>(`/auditorias/auditorias/${id}/concluir/`);
    return data;
  },

  // Obter relatório
  relatorio: async (id: number) => {
    const { data } = await api.get(`/auditorias/auditorias/${id}/relatorio/`);
    return data;
  },

  // Obter estatísticas
  estatisticas: async () => {
    const { data } = await api.get<Estatisticas>('/auditorias/auditorias/estatisticas/');
    return data;
  },
};

// Serviço de Constatações
export const constatacaoService = {
  // Listar constatações
  list: async (params?: any) => {
    const { data } = await api.get<PaginatedResponse<Constatacao>>('/auditorias/constatacoes/', { params });
    return data;
  },

  // Obter constatação por ID
  get: async (id: number) => {
    const { data } = await api.get<Constatacao>(`/auditorias/constatacoes/${id}/`);
    return data;
  },

  // Criar constatação
  create: async (constatacao: Partial<Constatacao>) => {
    const { data } = await api.post<Constatacao>('/auditorias/constatacoes/', constatacao);
    return data;
  },

  // Atualizar constatação
  update: async (id: number, constatacao: Partial<Constatacao>) => {
    const { data } = await api.patch<Constatacao>(`/auditorias/constatacoes/${id}/`, constatacao);
    return data;
  },

  // Deletar constatação
  delete: async (id: number) => {
    await api.delete(`/auditorias/constatacoes/${id}/`);
  },

  // Iniciar tratamento
  iniciarTratamento: async (id: number) => {
    const { data } = await api.post<Constatacao>(`/auditorias/constatacoes/${id}/iniciar_tratamento/`);
    return data;
  },

  // Solicitar validação
  solicitarValidacao: async (id: number) => {
    const { data } = await api.post<Constatacao>(`/auditorias/constatacoes/${id}/solicitar_validacao/`);
    return data;
  },

  // Fechar constatação
  fechar: async (id: number) => {
    const { data } = await api.post<Constatacao>(`/auditorias/constatacoes/${id}/fechar/`);
    return data;
  },
};

// Serviço de Ações Corretivas
export const acaoCorretivaService = {
  // Listar ações corretivas
  list: async (params?: any) => {
    const { data } = await api.get<PaginatedResponse<AcaoCorretiva>>('/auditorias/acoes-corretivas/', { params });
    return data;
  },

  // Obter ação corretiva por ID
  get: async (id: number) => {
    const { data } = await api.get<AcaoCorretiva>(`/auditorias/acoes-corretivas/${id}/`);
    return data;
  },

  // Criar ação corretiva
  create: async (acao: Partial<AcaoCorretiva>) => {
    const { data } = await api.post<AcaoCorretiva>('/auditorias/acoes-corretivas/', acao);
    return data;
  },

  // Atualizar ação corretiva
  update: async (id: number, acao: Partial<AcaoCorretiva>) => {
    const { data } = await api.patch<AcaoCorretiva>(`/auditorias/acoes-corretivas/${id}/`, acao);
    return data;
  },

  // Deletar ação corretiva
  delete: async (id: number) => {
    await api.delete(`/auditorias/acoes-corretivas/${id}/`);
  },

  // Iniciar ação
  iniciar: async (id: number) => {
    const { data } = await api.post<AcaoCorretiva>(`/auditorias/acoes-corretivas/${id}/iniciar/`);
    return data;
  },

  // Concluir ação
  concluir: async (id: number, evidencia_execucao: string) => {
    const { data } = await api.post<AcaoCorretiva>(
      `/auditorias/acoes-corretivas/${id}/concluir/`,
      { evidencia_execucao }
    );
    return data;
  },

  // Verificar ação
  verificar: async (id: number, eficaz: boolean, resultado_verificacao: string) => {
    const { data } = await api.post<AcaoCorretiva>(
      `/auditorias/acoes-corretivas/${id}/verificar/`,
      { eficaz, resultado_verificacao }
    );
    return data;
  },
};

// Serviço de Tipos de Auditoria
export const tipoAuditoriaService = {
  list: async () => {
    const { data } = await api.get<PaginatedResponse<TipoAuditoria>>('/auditorias/tipos-auditoria/');
    return data;
  },

  get: async (id: number) => {
    const { data } = await api.get<TipoAuditoria>(`/auditorias/tipos-auditoria/${id}/`);
    return data;
  },

  create: async (tipo: Partial<TipoAuditoria>) => {
    const { data } = await api.post<TipoAuditoria>('/auditorias/tipos-auditoria/', tipo);
    return data;
  },

  update: async (id: number, tipo: Partial<TipoAuditoria>) => {
    const { data } = await api.patch<TipoAuditoria>(`/auditorias/tipos-auditoria/${id}/`, tipo);
    return data;
  },

  delete: async (id: number) => {
    await api.delete(`/auditorias/tipos-auditoria/${id}/`);
  },
};

// Serviço de Tipos de Constatação
export const tipoConstatacaoService = {
  list: async () => {
    const { data } = await api.get<PaginatedResponse<TipoConstatacao>>('/auditorias/tipos-constatacao/');
    return data;
  },

  get: async (id: number) => {
    const { data } = await api.get<TipoConstatacao>(`/auditorias/tipos-constatacao/${id}/`);
    return data;
  },

  create: async (tipo: Partial<TipoConstatacao>) => {
    const { data } = await api.post<TipoConstatacao>('/auditorias/tipos-constatacao/', tipo);
    return data;
  },

  update: async (id: number, tipo: Partial<TipoConstatacao>) => {
    const { data } = await api.patch<TipoConstatacao>(`/auditorias/tipos-constatacao/${id}/`, tipo);
    return data;
  },

  delete: async (id: number) => {
    await api.delete(`/auditorias/tipos-constatacao/${id}/`);
  },
};

// Serviço de Processos
export const processoService = {
  list: async () => {
    const { data } = await api.get<PaginatedResponse<Processo>>('/auditorias/processos/');
    return data;
  },

  get: async (id: number) => {
    const { data } = await api.get<Processo>(`/auditorias/processos/${id}/`);
    return data;
  },

  create: async (processo: Partial<Processo>) => {
    const { data } = await api.post<Processo>('/auditorias/processos/', processo);
    return data;
  },

  update: async (id: number, processo: Partial<Processo>) => {
    const { data } = await api.patch<Processo>(`/auditorias/processos/${id}/`, processo);
    return data;
  },

  delete: async (id: number) => {
    await api.delete(`/auditorias/processos/${id}/`);
  },
};

// Serviço de Documentos
export const documentoService = {
  list: async (params?: any) => {
    const { data } = await api.get<PaginatedResponse<DocumentoAuditoria>>('/auditorias/documentos/', { params });
    return data;
  },

  get: async (id: number) => {
    const { data } = await api.get<DocumentoAuditoria>(`/auditorias/documentos/${id}/`);
    return data;
  },

  upload: async (formData: FormData) => {
    const { data } = await api.post<DocumentoAuditoria>('/auditorias/documentos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return data;
  },

  delete: async (id: number) => {
    await api.delete(`/auditorias/documentos/${id}/`);
  },
};

// Serviço de Comentários
export const comentarioService = {
  list: async (params?: any) => {
    const { data } = await api.get<PaginatedResponse<Comentario>>('/auditorias/comentarios/', { params });
    return data;
  },

  create: async (comentario: Partial<Comentario>) => {
    const { data } = await api.post<Comentario>('/auditorias/comentarios/', comentario);
    return data;
  },

  update: async (id: number, comentario: Partial<Comentario>) => {
    const { data } = await api.patch<Comentario>(`/auditorias/comentarios/${id}/`, comentario);
    return data;
  },

  delete: async (id: number) => {
    await api.delete(`/auditorias/comentarios/${id}/`);
  },
};
