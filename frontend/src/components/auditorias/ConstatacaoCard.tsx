import React from 'react';
import Link from 'next/link';
import { Constatacao } from '@/types';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import { formatDate, getStatusColor, getStatusLabel, getSeveridadeColor, getSeveridadeLabel } from '@/lib/utils';
import { Calendar, User, AlertCircle } from 'lucide-react';

interface ConstatacaoCardProps {
  constatacao: Constatacao;
}

const ConstatacaoCard: React.FC<ConstatacaoCardProps> = ({ constatacao }) => {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm text-gray-500">{constatacao.numero}</p>
            <CardTitle className="mt-1">{constatacao.titulo}</CardTitle>
          </div>
          <div className="flex flex-col space-y-1">
            <Badge className={getStatusColor(constatacao.status)}>
              {getStatusLabel(constatacao.status)}
            </Badge>
            {constatacao.tipo_detalhes && (
              <Badge className={getSeveridadeColor(constatacao.tipo_detalhes.severidade)}>
                {getSeveridadeLabel(constatacao.tipo_detalhes.severidade)}
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-3">
          {constatacao.tipo_detalhes && (
            <div className="flex items-center text-sm">
              <AlertCircle className="w-4 h-4 mr-2 text-gray-400" />
              <span className="text-gray-600">{constatacao.tipo_detalhes.nome}</span>
            </div>
          )}

          {constatacao.processo_detalhes && (
            <div className="flex items-center text-sm text-gray-600">
              <span className="font-medium mr-2">Processo:</span>
              <span>{constatacao.processo_detalhes.nome}</span>
            </div>
          )}

          {constatacao.responsavel_detalhes && (
            <div className="flex items-center text-sm text-gray-600">
              <User className="w-4 h-4 mr-2" />
              <span>
                {constatacao.responsavel_detalhes.first_name} {constatacao.responsavel_detalhes.last_name}
              </span>
            </div>
          )}

          <div className="flex items-center text-sm text-gray-600">
            <Calendar className="w-4 h-4 mr-2" />
            <span>Prazo: {formatDate(constatacao.prazo_resposta)}</span>
          </div>

          {constatacao.dias_em_aberto !== undefined && constatacao.dias_em_aberto > 0 && (
            <div className="text-sm text-orange-600">
              <span className="font-medium">{constatacao.dias_em_aberto} dias em aberto</span>
            </div>
          )}

          {constatacao.total_acoes !== undefined && (
            <div className="text-sm text-gray-600">
              <span>{constatacao.total_acoes} ação(ões) corretiva(s)</span>
            </div>
          )}
        </div>
      </CardContent>

      <CardFooter>
        <Link href={`/constatacoes/${constatacao.id}`} className="w-full">
          <Button variant="outline" className="w-full">
            Ver Detalhes
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
};

export default ConstatacaoCard;
