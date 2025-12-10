import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { Auditoria } from '@/types';
import { auditoriaService } from '@/services/auditoriaService';
import AuditoriaCard from '@/components/auditorias/AuditoriaCard';
import AuditoriaTable from '@/components/auditorias/AuditoriaTable';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Select from '@/components/ui/Select';
import { Plus, Search, Grid, List } from 'lucide-react';

export default function AuditoriasPage() {
  const [auditorias, setAuditorias] = useState<Auditoria[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  useEffect(() => {
    loadAuditorias();
  }, [statusFilter]);

  const loadAuditorias = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (statusFilter) params.status = statusFilter;
      const data = await auditoriaService.list(params);
      setAuditorias(data.results);
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar auditorias');
    } finally {
      setLoading(false);
    }
  };

  const filteredAuditorias = auditorias.filter((auditoria) => {
    const searchLower = searchTerm.toLowerCase();
    return (
      auditoria.codigo.toLowerCase().includes(searchLower) ||
      auditoria.titulo.toLowerCase().includes(searchLower) ||
      auditoria.descricao.toLowerCase().includes(searchLower)
    );
  });

  const handleDelete = async (id: number) => {
    if (!confirm('Tem certeza que deseja excluir esta auditoria?')) return;

    try {
      await auditoriaService.delete(id);
      loadAuditorias();
    } catch (err: any) {
      alert(err.message || 'Erro ao excluir auditoria');
    }
  };

  return (
    <>
      <Head>
        <title>Auditorias - SGQ Telco</title>
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <Link href="/" className="text-sm text-primary-600 hover:text-primary-700 mb-2 block">
                  ← Voltar ao Dashboard
                </Link>
                <h1 className="text-3xl font-bold text-gray-900">Auditorias</h1>
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
          {/* Filters */}
          <div className="bg-white p-4 rounded-lg shadow mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <Input
                  placeholder="Buscar por código, título ou descrição..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full"
                />
              </div>
              <div className="flex space-x-2">
                <Select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  options={[
                    { value: '', label: 'Todos os Status' },
                    { value: 'planejada', label: 'Planejada' },
                    { value: 'em_andamento', label: 'Em Andamento' },
                    { value: 'concluida', label: 'Concluída' },
                    { value: 'cancelada', label: 'Cancelada' },
                  ]}
                />
                <div className="flex space-x-1">
                  <Button
                    variant={viewMode === 'grid' ? 'primary' : 'ghost'}
                    size="sm"
                    onClick={() => setViewMode('grid')}
                  >
                    <Grid className="w-4 h-4" />
                  </Button>
                  <Button
                    variant={viewMode === 'list' ? 'primary' : 'ghost'}
                    size="sm"
                    onClick={() => setViewMode('list')}
                  >
                    <List className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </div>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Content */}
          {!loading && !error && (
            <>
              {filteredAuditorias.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-gray-500">Nenhuma auditoria encontrada</p>
                </div>
              ) : (
                <>
                  {viewMode === 'grid' ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {filteredAuditorias.map((auditoria) => (
                        <AuditoriaCard key={auditoria.id} auditoria={auditoria} />
                      ))}
                    </div>
                  ) : (
                    <div className="bg-white rounded-lg shadow">
                      <AuditoriaTable
                        auditorias={filteredAuditorias}
                        onDelete={handleDelete}
                      />
                    </div>
                  )}
                </>
              )}
            </>
          )}
        </main>
      </div>
    </>
  );
}
