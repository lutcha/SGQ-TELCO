from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Case, When, IntegerField
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import (
    Tenant, TipoAuditoria, Processo, Auditoria, TipoConstatacao,
    Constatacao, AcaoCorretiva, DocumentoAuditoria, Comentario, IndicadorAuditoria
)
from .serializers import (
    TenantSerializer, TipoAuditoriaSerializer, ProcessoSerializer,
    AuditoriaListSerializer, AuditoriaDetailSerializer, AuditoriaCreateUpdateSerializer,
    TipoConstatacaoSerializer, ConstatacaoListSerializer, ConstatacaoDetailSerializer,
    AcaoCorretivaSerializer, DocumentoAuditoriaSerializer, ComentarioSerializer,
    IndicadorAuditoriaSerializer, EstatisticasAuditoriaSerializer,
    AuditoriasPorMesSerializer, ConstatacoesPorTipoSerializer
)
from .permissions import IsTenantUser


class TenantViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Tenants"""
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'codigo']
    ordering_fields = ['nome', 'codigo', 'criado_em']
    ordering = ['nome']


class TipoAuditoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Tipos de Auditoria"""
    serializer_class = TipoAuditoriaSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['nome']
    filterset_fields = ['ativo']
    
    def get_queryset(self):
        return TipoAuditoria.objects.filter(tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)


class ProcessoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Processos"""
    serializer_class = ProcessoSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['codigo', 'nome', 'descricao']
    ordering_fields = ['codigo', 'nome', 'criado_em']
    ordering = ['codigo']
    filterset_fields = ['ativo', 'responsavel']
    
    def get_queryset(self):
        return Processo.objects.filter(tenant=self.request.user.tenant).select_related('responsavel')
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)


class TipoConstatacaoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Tipos de Constatação"""
    serializer_class = TipoConstatacaoSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'severidade', 'criado_em']
    ordering = ['-severidade', 'nome']
    filterset_fields = ['ativo', 'severidade', 'requer_acao']
    
    def get_queryset(self):
        return TipoConstatacao.objects.filter(tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)


class AuditoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Auditorias"""
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['codigo', 'titulo', 'descricao', 'objetivo', 'escopo']
    ordering_fields = ['codigo', 'titulo', 'data_planejada_inicio', 'data_planejada_fim', 'status', 'criado_em']
    ordering = ['-data_planejada_inicio']
    filterset_fields = ['status', 'tipo', 'auditor_lider', 'processos']
    
    def get_queryset(self):
        queryset = Auditoria.objects.filter(tenant=self.request.user.tenant).select_related(
            'tipo', 'auditor_lider', 'criado_por'
        ).prefetch_related('processos', 'equipe_auditores')
        
        # Filtros adicionais
        status_param = self.request.query_params.get('status', None)
        tipo_param = self.request.query_params.get('tipo', None)
        ano_param = self.request.query_params.get('ano', None)
        
        if status_param:
            queryset = queryset.filter(status=status_param)
        if tipo_param:
            queryset = queryset.filter(tipo_id=tipo_param)
        if ano_param:
            queryset = queryset.filter(data_planejada_inicio__year=ano_param)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AuditoriaListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AuditoriaCreateUpdateSerializer
        return AuditoriaDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            criado_por=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        """Iniciar uma auditoria"""
        auditoria = self.get_object()
        
        if auditoria.status != 'planejada':
            return Response(
                {'erro': 'Apenas auditorias planejadas podem ser iniciadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        auditoria.status = 'em_andamento'
        auditoria.data_real_inicio = timezone.now().date()
        auditoria.save()
        
        serializer = self.get_serializer(auditoria)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        """Concluir uma auditoria"""
        auditoria = self.get_object()
        
        if auditoria.status not in ['em_andamento', 'planejada']:
            return Response(
                {'erro': 'Apenas auditorias em andamento podem ser concluídas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        auditoria.status = 'concluida'
        auditoria.data_real_fim = timezone.now().date()
        auditoria.save()
        
        serializer = self.get_serializer(auditoria)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def relatorio(self, request, pk=None):
        """Gerar relatório da auditoria"""
        auditoria = self.get_object()
        constatacoes = auditoria.constatacoes.all().select_related(
            'tipo', 'processo', 'responsavel'
        ).prefetch_related('acoes_corretivas')
        
        relatorio = {
            'auditoria': AuditoriaDetailSerializer(auditoria).data,
            'resumo': {
                'total_constatacoes': constatacoes.count(),
                'constatacoes_por_tipo': {},
                'constatacoes_por_status': {},
                'constatacoes_por_processo': {},
            },
            'constatacoes': ConstatacaoListSerializer(constatacoes, many=True).data
        }
        
        # Estatísticas por tipo
        for tipo in constatacoes.values('tipo__nome').annotate(total=Count('id')):
            relatorio['resumo']['constatacoes_por_tipo'][tipo['tipo__nome']] = tipo['total']
        
        # Estatísticas por status
        for st in constatacoes.values('status').annotate(total=Count('id')):
            relatorio['resumo']['constatacoes_por_status'][st['status']] = st['total']
        
        # Estatísticas por processo
        for proc in constatacoes.values('processo__nome').annotate(total=Count('id')):
            relatorio['resumo']['constatacoes_por_processo'][proc['processo__nome']] = proc['total']
        
        return Response(relatorio)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Obter estatísticas gerais de auditorias"""
        tenant = request.user.tenant
        
        auditorias = Auditoria.objects.filter(tenant=tenant)
        constatacoes = Constatacao.objects.filter(tenant=tenant)
        
        total_constatacoes = constatacoes.count()
        constatacoes_abertas = constatacoes.filter(status='aberta').count()
        constatacoes_fechadas = constatacoes.filter(status='fechada').count()
        
        taxa_fechamento = Decimal(0)
        if total_constatacoes > 0:
            taxa_fechamento = Decimal(constatacoes_fechadas) / Decimal(total_constatacoes) * Decimal(100)
        
        # Constatações por severidade
        constatacoes_criticas = constatacoes.filter(tipo__severidade=4).count()
        constatacoes_altas = constatacoes.filter(tipo__severidade=3).count()
        
        # Ações atrasadas
        hoje = timezone.now().date()
        acoes_atrasadas = AcaoCorretiva.objects.filter(
            tenant=tenant,
            status__in=['planejada', 'em_andamento'],
            prazo_conclusao__lt=hoje
        ).count()
        
        stats = {
            'total_auditorias': auditorias.count(),
            'auditorias_planejadas': auditorias.filter(status='planejada').count(),
            'auditorias_em_andamento': auditorias.filter(status='em_andamento').count(),
            'auditorias_concluidas': auditorias.filter(status='concluida').count(),
            'total_constatacoes': total_constatacoes,
            'constatacoes_abertas': constatacoes_abertas,
            'constatacoes_fechadas': constatacoes_fechadas,
            'taxa_fechamento': round(taxa_fechamento, 2),
            'constatacoes_criticas': constatacoes_criticas,
            'constatacoes_altas': constatacoes_altas,
            'acoes_atrasadas': acoes_atrasadas,
        }
        
        serializer = EstatisticasAuditoriaSerializer(stats)
        return Response(serializer.data)


class ConstatacaoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Constatações"""
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['numero', 'titulo', 'descricao', 'evidencia']
    ordering_fields = ['numero', 'titulo', 'prazo_resposta', 'status', 'criado_em']
    ordering = ['-criado_em']
    filterset_fields = ['status', 'tipo', 'processo', 'auditoria', 'responsavel']
    
    def get_queryset(self):
        return Constatacao.objects.filter(tenant=self.request.user.tenant).select_related(
            'tipo', 'processo', 'auditoria', 'responsavel', 'criado_por'
        ).prefetch_related('acoes_corretivas')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConstatacaoListSerializer
        return ConstatacaoDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            criado_por=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def iniciar_tratamento(self, request, pk=None):
        """Iniciar tratamento de uma constatação"""
        constatacao = self.get_object()
        
        if constatacao.status != 'aberta':
            return Response(
                {'erro': 'Apenas constatações abertas podem iniciar tratamento'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        constatacao.status = 'em_tratamento'
        constatacao.save()
        
        serializer = self.get_serializer(constatacao)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def solicitar_validacao(self, request, pk=None):
        """Solicitar validação de uma constatação"""
        constatacao = self.get_object()
        
        if constatacao.status != 'em_tratamento':
            return Response(
                {'erro': 'Apenas constatações em tratamento podem solicitar validação'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se há ações corretivas concluídas
        acoes_pendentes = constatacao.acoes_corretivas.exclude(status='concluida').count()
        if acoes_pendentes > 0:
            return Response(
                {'erro': f'Há {acoes_pendentes} ação(ões) pendente(s)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        constatacao.status = 'aguardando_validacao'
        constatacao.save()
        
        serializer = self.get_serializer(constatacao)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def fechar(self, request, pk=None):
        """Fechar uma constatação"""
        constatacao = self.get_object()
        
        if constatacao.status != 'aguardando_validacao':
            return Response(
                {'erro': 'Apenas constatações aguardando validação podem ser fechadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        constatacao.status = 'fechada'
        constatacao.data_fechamento = timezone.now().date()
        constatacao.save()
        
        serializer = self.get_serializer(constatacao)
        return Response(serializer.data)


class AcaoCorretivaViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Ações Corretivas"""
    serializer_class = AcaoCorretivaSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['numero', 'descricao', 'objetivo']
    ordering_fields = ['numero', 'prazo_conclusao', 'status', 'criado_em']
    ordering = ['-criado_em']
    filterset_fields = ['status', 'tipo', 'constatacao', 'responsavel', 'eficaz']
    
    def get_queryset(self):
        return AcaoCorretiva.objects.filter(tenant=self.request.user.tenant).select_related(
            'constatacao', 'responsavel', 'verificada_por', 'criado_por'
        )
    
    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            criado_por=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        """Iniciar execução de uma ação corretiva"""
        acao = self.get_object()
        
        if acao.status != 'planejada':
            return Response(
                {'erro': 'Apenas ações planejadas podem ser iniciadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        acao.status = 'em_andamento'
        acao.save()
        
        serializer = self.get_serializer(acao)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        """Concluir uma ação corretiva"""
        acao = self.get_object()
        
        if acao.status not in ['planejada', 'em_andamento']:
            return Response(
                {'erro': 'Apenas ações em andamento podem ser concluídas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        evidencia = request.data.get('evidencia_execucao', '')
        if not evidencia:
            return Response(
                {'erro': 'É necessário informar a evidência de execução'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        acao.status = 'concluida'
        acao.data_conclusao = timezone.now().date()
        acao.evidencia_execucao = evidencia
        acao.save()
        
        serializer = self.get_serializer(acao)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def verificar(self, request, pk=None):
        """Verificar eficácia de uma ação corretiva"""
        acao = self.get_object()
        
        if acao.status != 'concluida':
            return Response(
                {'erro': 'Apenas ações concluídas podem ser verificadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        eficaz = request.data.get('eficaz')
        resultado = request.data.get('resultado_verificacao', '')
        
        if eficaz is None:
            return Response(
                {'erro': 'É necessário informar se a ação foi eficaz'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not resultado:
            return Response(
                {'erro': 'É necessário informar o resultado da verificação'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        acao.status = 'verificada'
        acao.verificada_por = request.user
        acao.data_verificacao = timezone.now().date()
        acao.resultado_verificacao = resultado
        acao.eficaz = eficaz
        acao.save()
        
        serializer = self.get_serializer(acao)
        return Response(serializer.data)


class DocumentoAuditoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Documentos de Auditoria"""
    serializer_class = DocumentoAuditoriaSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'enviado_em']
    ordering = ['-enviado_em']
    filterset_fields = ['tipo', 'auditoria', 'constatacao']
    
    def get_queryset(self):
        return DocumentoAuditoria.objects.filter(tenant=self.request.user.tenant).select_related(
            'auditoria', 'constatacao', 'enviado_por'
        )
    
    def perform_create(self, serializer):
        arquivo = self.request.FILES.get('arquivo')
        tamanho = arquivo.size if arquivo else 0
        
        serializer.save(
            tenant=self.request.user.tenant,
            enviado_por=self.request.user,
            tamanho=tamanho
        )


class ComentarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Comentários"""
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['criado_em']
    ordering = ['criado_em']
    filterset_fields = ['auditoria', 'constatacao', 'autor']
    
    def get_queryset(self):
        return Comentario.objects.filter(tenant=self.request.user.tenant).select_related(
            'auditoria', 'constatacao', 'autor'
        )
    
    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            autor=self.request.user
        )


class IndicadorAuditoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Indicadores de Auditoria"""
    serializer_class = IndicadorAuditoriaSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['nome']
    filterset_fields = ['ativo']
    
    def get_queryset(self):
        return IndicadorAuditoria.objects.filter(tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)
