import React from 'react';
import Link from 'next/link';
import { Auditoria } from '@/types';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import { formatDate, getStatusColor, getStatusLabel } from '@/lib/utils';
import { Calendar, Users, FileText, CheckCircle, XCircle } from 'lucide-react';

interface AuditoriaCardProps {
  auditoria: Auditoria;
}

const AuditoriaCard: React.FC<AuditoriaCardProps> = ({ auditoria }) => {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm text-gray-500">{auditoria.codigo}</p>
            <CardTitle className="mt-1">{auditoria.titulo}</CardTitle>
          </div>
          <Badge className={getStatusColor(auditoria.status)}>
            {getStatusLabel(auditoria.status)}
          </Badge>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-3">
          {auditoria.tipo_detalhes && (
            <div className="flex items-center text-sm">
              <div
                className="w-3 h-3 rounded-full mr-2"
                style={{ backgroundColor: auditoria.tipo_detalhes.cor }}
              />
              <span className="text-gray-600">{auditoria.tipo_detalhes.nome}</span>
            </div>
          )}

          <div className="flex items-center text-sm text-gray-600">
            <Calendar className="w-4 h-4 mr-2" />
            <span>
              {formatDate(auditoria.data_planejada_inicio)} - {formatDate(auditoria.data_planejada_fim)}
            </span>
          </div>

          {auditoria.auditor_lider_detalhes && (
            <div className="flex items-center text-sm text-gray-600">
              <Users className="w-4 h-4 mr-2" />
              <span>
                {auditoria.auditor_lider_detalhes.first_name} {auditoria.auditor_lider_detalhes.last_name}
              </span>
            </div>
          )}

          <div className="flex items-center justify-between pt-3 border-t">
            <div className="flex items-center text-sm">
              <FileText className="w-4 h-4 mr-1 text-gray-400" />
              <span className="text-gray-600">{auditoria.total_constatacoes || 0} constatações</span>
            </div>
            <div className="flex space-x-2">
              <div className="flex items-center text-sm text-green-600">
                <CheckCircle className="w-4 h-4 mr-1" />
                <span>{auditoria.constatacoes_fechadas || 0}</span>
              </div>
              <div className="flex items-center text-sm text-red-600">
                <XCircle className="w-4 h-4 mr-1" />
                <span>{auditoria.constatacoes_abertas || 0}</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>

      <CardFooter>
        <Link href={`/auditorias/${auditoria.id}`} className="w-full">
          <Button variant="outline" className="w-full">
            Ver Detalhes
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
};

export default AuditoriaCard;
