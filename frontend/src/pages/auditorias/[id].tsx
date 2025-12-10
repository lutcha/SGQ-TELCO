import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Auditoria } from '@/types';
import { auditoriaService } from '@/services/auditoriaService';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import ConstatacaoCard from '@/components/auditorias/ConstatacaoCard';
import { formatDate, getStatusColor, getStatusLabel } from '@/lib/utils';
import { Calendar, Users, FileText, CheckCircle, Play, CheckSquare } from 'lucide-react';

export default function AuditoriaDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const [auditoria, setAuditoria] = useState<Auditoria | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadAuditoria();
    }
  }, [id]);

  const loadAuditoria = async () => {
    try {
      setLoading(true);
      const data = await auditoriaService.get(Number(id));
      setAuditoria(data);
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar auditoria');
    } finally {
      setLoading(false);
    }
  };

  const handleIniciar = async () => {
    if (!auditoria) return;
    try {
      await auditoriaService.iniciar(auditoria.id);
      loadAuditoria();
    } catch (err: any) {
      alert(err.message || 'Erro ao iniciar auditoria');
    }
  };

  const handleConcluir = async () => {
    if (!auditoria) return;
    if (!confirm('Tem certeza que deseja concluir esta auditoria?')) return;
    try {
      await auditoriaService.concluir(auditoria.id);
      loadAuditoria();
    } catch (err: any) {
      alert(err.message || 'Erro ao concluir auditoria');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !auditoria) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Auditoria não encontrada'}</p>
          <Link href="/auditorias">
            <Button>Voltar para Auditorias</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{auditoria.codigo} - {auditoria.titulo}</title>
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <Link href="/auditorias" className="text-sm text-primary-600 hover:text-primary-700 mb-2 block">
              ← Voltar para Auditorias
            </Link>
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-gray-500">{auditoria.codigo}</p>
                <h1 className="text-3xl font-bold text-gray-900 mt-1">{auditoria.titulo}</h1>
              </div>
              <div className="flex space-x-2">
                <Badge className={getStatusColor(auditoria.status)}>
                  {getStatusLabel(auditoria.status)}
                </Badge>
                {auditoria.status === 'planejada' && (
                  <Button onClick={handleIniciar} size="sm">
                    <Play className="w-4 h-4 mr-2" />
                    Iniciar
                  </Button>
                )}
                {auditoria.status === 'em_andamento' && (
                  <Button onClick={handleConcluir} size="sm" variant="success">
                    <CheckSquare className="w-4 h-4 mr-2" />
                    Concluir
                  </Button>
                )}
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Info */}
            <div className="lg:col-span-2 space-y-6">
              {/* Informações Básicas */}
              <Card>
                <CardHeader>
                  <CardTitle>Informações da Auditoria</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {auditoria.tipo_detalhes && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Tipo</label>
                      <div className="flex items-center mt-1">
                        <div
                          className="w-3 h-3 rounded-full mr-2"
                          style={{ backgroundColor: auditoria.tipo_detalhes.cor }}
                        />
                        <span>{auditoria.tipo_detalhes.nome}</span>
                      </div>
                    </div>
                  )}

                  <div>
                    <label className="text-sm font-medium text-gray-600">Objetivo</label>
                    <p className="mt-1 text-gray-900">{auditoria.objetivo}</p>
                  </div>

                  <div>
                    <label className="text-sm font-medium text-gray-600">Escopo</label>
                    <p className="mt-1 text-gray-900">{auditoria.escopo}</p>
                  </div>

                  {auditoria.descricao && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Descrição</label>
                      <p className="mt-1 text-gray-900">{auditoria.descricao}</p>
                    </div>
                  )}

                  {auditoria.norma_referencia && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Norma de Referência</label>
                      <p className="mt-1 text-gray-900">{auditoria.norma_referencia}</p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Constatações */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Constatações</CardTitle>
                    <Link href={`/constatacoes/nova?auditoria=${auditoria.id}`}>
                      <Button size="sm">
                        <FileText className="w-4 h-4 mr-2" />
                        Nova Constatação
                      </Button>
                    </Link>
                  </div>
                </CardHeader>
                <CardContent>
                  {auditoria.constatacoes && auditoria.constatacoes.length > 0 ? (
                    <div className="grid grid-cols-1 gap-4">
                      {auditoria.constatacoes.map((constatacao) => (
                        <ConstatacaoCard key={constatacao.id} constatacao={constatacao} />
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-8">
                      Nenhuma constatação registrada
                    </p>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Datas */}
              <Card>
                <CardHeader>
                  <CardTitle>Datas</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div>
                    <label className="text-sm font-medium text-gray-600">Planejado</label>
                    <div className="flex items-center text-sm text-gray-900 mt-1">
                      <Calendar className="w-4 h-4 mr-2" />
                      <span>
                        {formatDate(auditoria.data_planejada_inicio)} -{' '}
                        {formatDate(auditoria.data_planejada_fim)}
                      </span>
                    </div>
                  </div>
                  {auditoria.data_real_inicio && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Real</label>
                      <div className="flex items-center text-sm text-gray-900 mt-1">
                        <Calendar className="w-4 h-4 mr-2" />
                        <span>
                          {formatDate(auditoria.data_real_inicio)}
                          {auditoria.data_real_fim && ` - ${formatDate(auditoria.data_real_fim)}`}
                        </span>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Equipe */}
              <Card>
                <CardHeader>
                  <CardTitle>Equipe</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {auditoria.auditor_lider_detalhes && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Auditor Líder</label>
                      <div className="flex items-center text-sm text-gray-900 mt-1">
                        <Users className="w-4 h-4 mr-2" />
                        <span>
                          {auditoria.auditor_lider_detalhes.first_name}{' '}
                          {auditoria.auditor_lider_detalhes.last_name}
                        </span>
                      </div>
                    </div>
                  )}
                  {auditoria.equipe_auditores_detalhes && auditoria.equipe_auditores_detalhes.length > 0 && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">Equipe</label>
                      <ul className="mt-1 space-y-1">
                        {auditoria.equipe_auditores_detalhes.map((auditor) => (
                          <li key={auditor.id} className="text-sm text-gray-900">
                            • {auditor.first_name} {auditor.last_name}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Estatísticas */}
              <Card>
                <CardHeader>
                  <CardTitle>Estatísticas</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Total de Constatações</span>
                    <span className="font-semibold">{auditoria.total_constatacoes || 0}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-green-600">Fechadas</span>
                    <span className="font-semibold text-green-600">
                      {auditoria.constatacoes_fechadas || 0}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-red-600">Abertas</span>
                    <span className="font-semibold text-red-600">
                      {auditoria.constatacoes_abertas || 0}
                    </span>
                  </div>
                </CardContent>
              </Card>

              {/* Processos */}
              {auditoria.processos_detalhes && auditoria.processos_detalhes.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Processos Auditados</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {auditoria.processos_detalhes.map((processo) => (
                        <li key={processo.id} className="text-sm">
                          <span className="font-medium">{processo.codigo}</span> - {processo.nome}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </main>
      </div>
    </>
  );
}
