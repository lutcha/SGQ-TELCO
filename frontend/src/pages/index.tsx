import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { Estatisticas } from '@/types';
import { auditoriaService } from '@/services/auditoriaService';
import Dashboard from '@/components/auditorias/Dashboard';
import Button from '@/components/ui/Button';
import { Plus } from 'lucide-react';

export default function Home() {
  const [estatisticas, setEstatisticas] = useState<Estatisticas | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadEstatisticas();
  }, []);

  const loadEstatisticas = async () => {
    try {
      setLoading(true);
      const data = await auditoriaService.estatisticas();
      setEstatisticas(data);
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar estatísticas');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>SGQ Telco - Dashboard de Auditorias</title>
        <meta name="description" content="Sistema de Gestão de Qualidade Telco - Módulo de Auditorias" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Dashboard de Auditorias</h1>
                <p className="text-gray-600 mt-1">Sistema de Gestão de Qualidade Telco</p>
              </div>
              <Link href="/auditorias/nova">
                <Button>
                  <Plus className="w-4 h-4 mr-2" />
                  Nova Auditoria
                </Button>
              </Link>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {loading && (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {estatisticas && !loading && !error && (
            <Dashboard estatisticas={estatisticas} />
          )}

          {/* Quick Links */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link
              href="/auditorias"
              className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Auditorias</h3>
              <p className="text-gray-600">Visualizar e gerenciar todas as auditorias</p>
            </Link>

            <Link
              href="/constatacoes"
              className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Constatações</h3>
              <p className="text-gray-600">Acompanhar constatações e achados</p>
            </Link>

            <Link
              href="/acoes-corretivas"
              className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Ações Corretivas</h3>
              <p className="text-gray-600">Gerenciar ações corretivas e preventivas</p>
            </Link>
          </div>
        </main>
      </div>
    </>
  );
}
