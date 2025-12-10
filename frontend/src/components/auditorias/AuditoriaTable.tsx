import React from 'react';
import Link from 'next/link';
import { Auditoria } from '@/types';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import { formatDate, getStatusColor, getStatusLabel } from '@/lib/utils';
import { Eye, Edit, Trash2 } from 'lucide-react';

interface AuditoriaTableProps {
  auditorias: Auditoria[];
  onEdit?: (id: number) => void;
  onDelete?: (id: number) => void;
}

const AuditoriaTable: React.FC<AuditoriaTableProps> = ({ auditorias, onEdit, onDelete }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Código
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Título
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Tipo
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Auditor Líder
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Data Início
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Constatações
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Ações
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {auditorias.map((auditoria) => (
            <tr key={auditoria.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {auditoria.codigo}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {auditoria.titulo}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm">
                {auditoria.tipo_detalhes && (
                  <div className="flex items-center">
                    <div
                      className="w-2 h-2 rounded-full mr-2"
                      style={{ backgroundColor: auditoria.tipo_detalhes.cor }}
                    />
                    <span>{auditoria.tipo_detalhes.nome}</span>
                  </div>
                )}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <Badge className={getStatusColor(auditoria.status)}>
                  {getStatusLabel(auditoria.status)}
                </Badge>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {auditoria.auditor_lider_detalhes
                  ? `${auditoria.auditor_lider_detalhes.first_name} ${auditoria.auditor_lider_detalhes.last_name}`
                  : '-'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {formatDate(auditoria.data_planejada_inicio)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <div className="flex space-x-2">
                  <span className="text-green-600">{auditoria.constatacoes_fechadas || 0}</span>
                  <span className="text-gray-400">/</span>
                  <span className="text-gray-900">{auditoria.total_constatacoes || 0}</span>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex justify-end space-x-2">
                  <Link href={`/auditorias/${auditoria.id}`}>
                    <Button variant="ghost" size="sm">
                      <Eye className="w-4 h-4" />
                    </Button>
                  </Link>
                  {onEdit && (
                    <Button variant="ghost" size="sm" onClick={() => onEdit(auditoria.id)}>
                      <Edit className="w-4 h-4" />
                    </Button>
                  )}
                  {onDelete && (
                    <Button variant="ghost" size="sm" onClick={() => onDelete(auditoria.id)}>
                      <Trash2 className="w-4 h-4 text-red-600" />
                    </Button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AuditoriaTable;
