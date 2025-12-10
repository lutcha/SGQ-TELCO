import React from 'react';
import { Estatisticas } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { FileText, CheckCircle, XCircle, AlertTriangle, Clock } from 'lucide-react';

interface DashboardProps {
  estatisticas: Estatisticas;
}

const Dashboard: React.FC<DashboardProps> = ({ estatisticas }) => {
  const cards = [
    {
      title: 'Total de Auditorias',
      value: estatisticas.total_auditorias,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Em Andamento',
      value: estatisticas.auditorias_em_andamento,
      icon: Clock,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
    },
    {
      title: 'Concluídas',
      value: estatisticas.auditorias_concluidas,
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Planejadas',
      value: estatisticas.auditorias_planejadas,
      icon: FileText,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
  ];

  const constatacaoCards = [
    {
      title: 'Total de Constatações',
      value: estatisticas.total_constatacoes,
      icon: FileText,
      color: 'text-gray-600',
      bgColor: 'bg-gray-100',
    },
    {
      title: 'Constatações Abertas',
      value: estatisticas.constatacoes_abertas,
      icon: XCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      title: 'Constatações Fechadas',
      value: estatisticas.constatacoes_fechadas,
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Taxa de Fechamento',
      value: `${estatisticas.taxa_fechamento}%`,
      icon: CheckCircle,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
  ];

  const alertCards = [
    {
      title: 'Constatações Críticas',
      value: estatisticas.constatacoes_criticas,
      icon: AlertTriangle,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      title: 'Constatações Altas',
      value: estatisticas.constatacoes_altas,
      icon: AlertTriangle,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
    {
      title: 'Ações Atrasadas',
      value: estatisticas.acoes_atrasadas,
      icon: Clock,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Auditorias */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Visão Geral de Auditorias</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {cards.map((card) => {
            const Icon = card.icon;
            return (
              <Card key={card.title}>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">{card.title}</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">{card.value}</p>
                    </div>
                    <div className={`p-3 rounded-lg ${card.bgColor}`}>
                      <Icon className={`w-6 h-6 ${card.color}`} />
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Constatações */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Constatações</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {constatacaoCards.map((card) => {
            const Icon = card.icon;
            return (
              <Card key={card.title}>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">{card.title}</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">{card.value}</p>
                    </div>
                    <div className={`p-3 rounded-lg ${card.bgColor}`}>
                      <Icon className={`w-6 h-6 ${card.color}`} />
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Alertas */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Alertas e Atenção</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {alertCards.map((card) => {
            const Icon = card.icon;
            return (
              <Card key={card.title}>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">{card.title}</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">{card.value}</p>
                    </div>
                    <div className={`p-3 rounded-lg ${card.bgColor}`}>
                      <Icon className={`w-6 h-6 ${card.color}`} />
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
