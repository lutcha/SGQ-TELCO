import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { format, formatDistanceToNow, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// Função para combinar classes CSS
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Funções de formatação de data
export function formatDate(date: string | Date, formatStr = 'dd/MM/yyyy'): string {
  const dateObj = typeof date === 'string' ? parseISO(date) : date;
  return format(dateObj, formatStr, { locale: ptBR });
}

export function formatDateTime(date: string | Date): string {
  return formatDate(date, 'dd/MM/yyyy HH:mm');
}

export function formatRelativeDate(date: string | Date): string {
  const dateObj = typeof date === 'string' ? parseISO(date) : date;
  return formatDistanceToNow(dateObj, { addSuffix: true, locale: ptBR });
}

// Funções para status
export const getStatusColor = (status: string): string => {
  const colors: Record<string, string> = {
    planejada: 'bg-blue-100 text-blue-800',
    em_andamento: 'bg-yellow-100 text-yellow-800',
    concluida: 'bg-green-100 text-green-800',
    cancelada: 'bg-gray-100 text-gray-800',
    aberta: 'bg-red-100 text-red-800',
    em_tratamento: 'bg-orange-100 text-orange-800',
    aguardando_validacao: 'bg-blue-100 text-blue-800',
    fechada: 'bg-green-100 text-green-800',
    verificada: 'bg-teal-100 text-teal-800',
  };
  return colors[status] || 'bg-gray-100 text-gray-800';
};

export const getStatusLabel = (status: string): string => {
  const labels: Record<string, string> = {
    planejada: 'Planejada',
    em_andamento: 'Em Andamento',
    concluida: 'Concluída',
    cancelada: 'Cancelada',
    aberta: 'Aberta',
    em_tratamento: 'Em Tratamento',
    aguardando_validacao: 'Aguardando Validação',
    fechada: 'Fechada',
    verificada: 'Verificada',
  };
  return labels[status] || status;
};

// Função para severidade
export const getSeveridadeColor = (severidade: number): string => {
  const colors: Record<number, string> = {
    1: 'bg-blue-100 text-blue-800',
    2: 'bg-yellow-100 text-yellow-800',
    3: 'bg-orange-100 text-orange-800',
    4: 'bg-red-100 text-red-800',
  };
  return colors[severidade] || 'bg-gray-100 text-gray-800';
};

export const getSeveridadeLabel = (severidade: number): string => {
  const labels: Record<number, string> = {
    1: 'Baixa',
    2: 'Média',
    3: 'Alta',
    4: 'Crítica',
  };
  return labels[severidade] || '';
};

// Função para formatar tamanho de arquivo
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Função para calcular dias entre datas
export function daysBetween(date1: string | Date, date2: string | Date): number {
  const d1 = typeof date1 === 'string' ? parseISO(date1) : date1;
  const d2 = typeof date2 === 'string' ? parseISO(date2) : date2;
  const diffTime = Math.abs(d2.getTime() - d1.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

// Função para verificar se está atrasado
export function isOverdue(date: string | Date): boolean {
  const dateObj = typeof date === 'string' ? parseISO(date) : date;
  return dateObj < new Date();
}

// Função para truncar texto
export function truncate(text: string, length: number): string {
  if (text.length <= length) return text;
  return text.substring(0, length) + '...';
}

// Função para gerar cor aleatória
export function getRandomColor(): string {
  const colors = [
    '#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0',
    '#00BCD4', '#FFEB3B', '#8BC34A', '#FF5722', '#607D8B'
  ];
  return colors[Math.floor(Math.random() * colors.length)];
}
