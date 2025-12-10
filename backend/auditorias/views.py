from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import AuditoriaFilter, ProgramaAuditoriaFilter
from .models import (
    Auditoria,
    AuditoriaStatus,
    ChecklistAuditoria,
    Constatacao,
    PlanoAuditoria,
    ProgramaAuditoria,
    RelatorioAuditoria,
    SeguimentoAuditoria,
)
from .permissions import RolePermission, UserRoles
from .serializers import (
    AuditoriaDetailSerializer,
    AuditoriaSerializer,
    ChecklistAuditoriaSerializer,
    ConstatacaoSerializer,
    DashboardResponseSerializer,
    PlanoAuditoriaSerializer,
    ProgramaAuditoriaSerializer,
    RelatorioAuditoriaSerializer,
    SeguimentoAuditoriaSerializer,
)
from .services import build_dashboard_payload, calculate_kpis, generate_relatorio_pdf, transition_auditoria


class ProgramaAuditoriaViewSet(viewsets.ModelViewSet):
    queryset = ProgramaAuditoria.objects.select_related('elaborado_por', 'aprovado_por')
    serializer_class = ProgramaAuditoriaSerializer
    permission_classes = [RolePermission]
    filterset_class = ProgramaAuditoriaFilter
    search_fields = ['versao', 'observacoes']
    ordering_fields = ['ano', 'versao', 'status', 'criado_em']

    role_permissions = {
        'list': [UserRoles.ADMIN, UserRoles.DIRETOR, UserRoles.GESTOR],
        'retrieve': [UserRoles.ADMIN, UserRoles.DIRETOR, UserRoles.GESTOR],
        'create': [UserRoles.ADMIN, UserRoles.GESTOR],
        'update': [UserRoles.ADMIN, UserRoles.GESTOR],
        'partial_update': [UserRoles.ADMIN, UserRoles.GESTOR],
        'destroy': [UserRoles.ADMIN],
    }

    def perform_create(self, serializer):
        serializer.save(elaborado_por=self.request.user)


class AuditoriaViewSet(viewsets.ModelViewSet):
    queryset = Auditoria.objects.select_related(
        'programa', 'auditor_lider', 'criado_por'
    ).prefetch_related('processos', 'departamentos', 'auditores')
    serializer_class = AuditoriaSerializer
    permission_classes = [RolePermission]
    filterset_class = AuditoriaFilter
    search_fields = ['numero_sequencial', 'ambito']
    ordering_fields = ['data_prevista_inicio', 'status', 'tipo', 'criado_em']

    role_permissions = {
        'list': [
            UserRoles.ADMIN,
            UserRoles.DIRETOR,
            UserRoles.GESTOR,
            UserRoles.AUDITOR,
            UserRoles.PROCESS_OWNER,
        ],
        'retrieve': [
            UserRoles.ADMIN,
            UserRoles.DIRETOR,
            UserRoles.GESTOR,
            UserRoles.AUDITOR,
            UserRoles.PROCESS_OWNER,
            UserRoles.COLABORADOR,
        ],
        'create': [UserRoles.ADMIN, UserRoles.GESTOR],
        'update': [UserRoles.ADMIN, UserRoles.GESTOR],
        'partial_update': [UserRoles.ADMIN, UserRoles.GESTOR],
        'destroy': [UserRoles.ADMIN],
        'iniciar': [UserRoles.ADMIN, UserRoles.GESTOR],
        'concluir': [UserRoles.ADMIN, UserRoles.GESTOR],
        'cancelar': [UserRoles.ADMIN, UserRoles.GESTOR],
        'plano': [UserRoles.ADMIN, UserRoles.GESTOR, UserRoles.AUDITOR],
        'checklists': [UserRoles.ADMIN, UserRoles.GESTOR, UserRoles.AUDITOR],
        'checklist_detail': [UserRoles.ADMIN, UserRoles.GESTOR, UserRoles.AUDITOR],
        'constatacoes': [UserRoles.ADMIN, UserRoles.GESTOR, UserRoles.AUDITOR],
        'relatorio': [UserRoles.ADMIN, UserRoles.GESTOR, UserRoles.AUDITOR],
        'relatorio_gerar_pdf': [UserRoles.ADMIN, UserRoles.GESTOR],
        'seguimento': [UserRoles.ADMIN, UserRoles.GESTOR],
        'stats': [UserRoles.ADMIN, UserRoles.DIRETOR, UserRoles.GESTOR],
        'dashboard': [UserRoles.ADMIN, UserRoles.DIRETOR, UserRoles.GESTOR],
    }

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuditoriaDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)

    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        auditoria = self.get_object()
        transition_auditoria(auditoria, novo_status=AuditoriaStatus.EM_EXECUCAO)
        return Response({'status': 'auditoria iniciada'})

    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        auditoria = self.get_object()
        transition_auditoria(auditoria, novo_status=AuditoriaStatus.CONCLUIDA)
        return Response({'status': 'auditoria concluída'})

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        auditoria = self.get_object()
        transition_auditoria(auditoria, novo_status=AuditoriaStatus.CANCELADA)
        return Response({'status': 'auditoria cancelada'})

    @action(detail=True, methods=['get', 'post', 'put'], url_path='plano')
    def plano(self, request, pk=None):
        auditoria = self.get_object()
        try:
            plano = auditoria.plano
        except PlanoAuditoria.DoesNotExist:
            plano = None

        if request.method == 'GET':
            if not plano:
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer = PlanoAuditoriaSerializer(plano)
            return Response(serializer.data)

        data = request.data.copy()
        if request.method == 'POST':
            if plano:
                return Response({'detail': 'Plano já existe.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = PlanoAuditoriaSerializer(data=data)
            if serializer.is_valid():
                serializer.save(auditoria=auditoria)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = PlanoAuditoriaSerializer(plano, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], url_path='checklists')
    def checklists(self, request, pk=None):
        auditoria = self.get_object()
        if request.method == 'GET':
            serializer = ChecklistAuditoriaSerializer(auditoria.checklists.all(), many=True)
            return Response(serializer.data)
        serializer = ChecklistAuditoriaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(auditoria=auditoria)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'put'], url_path='checklists/(?P<checklist_id>[^/.]+)')
    def checklist_detail(self, request, pk=None, checklist_id=None):
        checklist = get_object_or_404(ChecklistAuditoria, pk=checklist_id, auditoria_id=pk)
        if request.method == 'GET':
            serializer = ChecklistAuditoriaSerializer(checklist)
            return Response(serializer.data)
        serializer = ChecklistAuditoriaSerializer(checklist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], url_path='constatacoes')
    def constatacoes(self, request, pk=None):
        auditoria = self.get_object()
        if request.method == 'GET':
            serializer = ConstatacaoSerializer(auditoria.constatacoes.all(), many=True)
            return Response(serializer.data)
        serializer = ConstatacaoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(auditoria=auditoria)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post', 'put'], url_path='relatorio')
    def relatorio(self, request, pk=None):
        auditoria = self.get_object()
        relatorio = getattr(auditoria, 'relatorio', None)
        if request.method == 'GET':
            if not relatorio:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(RelatorioAuditoriaSerializer(relatorio).data)

        if request.method == 'POST':
            if relatorio:
                return Response({'detail': 'Relatório já existe.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = RelatorioAuditoriaSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(auditoria=auditoria)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer = RelatorioAuditoriaSerializer(relatorio, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='relatorio/gerar-pdf')
    def relatorio_gerar_pdf(self, request, pk=None):
        auditoria = self.get_object()
        relatorio = getattr(auditoria, 'relatorio', None)
        if not relatorio:
            return Response({'detail': 'Crie o relatório antes de gerar o PDF.'}, status=status.HTTP_400_BAD_REQUEST)
        url = generate_relatorio_pdf(relatorio)
        return Response({'arquivo_pdf': url})

    @action(detail=True, methods=['get', 'post', 'put'], url_path='seguimento')
    def seguimento(self, request, pk=None):
        auditoria = self.get_object()
        seguimento = getattr(auditoria, 'seguimento', None)
        if request.method == 'GET':
            if not seguimento:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(SeguimentoAuditoriaSerializer(seguimento).data)

        if request.method == 'POST':
            if seguimento:
                return Response({'detail': 'Seguimento já existe.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = SeguimentoAuditoriaSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(auditoria=auditoria)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer = SeguimentoAuditoriaSerializer(seguimento, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        return Response(calculate_kpis())

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        payload = build_dashboard_payload()
        serializer = DashboardResponseSerializer(payload)
        return Response(serializer.data)
