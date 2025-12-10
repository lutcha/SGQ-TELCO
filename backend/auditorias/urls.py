from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TenantViewSet, TipoAuditoriaViewSet, ProcessoViewSet, AuditoriaViewSet,
    TipoConstatacaoViewSet, ConstatacaoViewSet, AcaoCorretivaViewSet,
    DocumentoAuditoriaViewSet, ComentarioViewSet, IndicadorAuditoriaViewSet
)

app_name = 'auditorias'

router = DefaultRouter()
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'tipos-auditoria', TipoAuditoriaViewSet, basename='tipo-auditoria')
router.register(r'processos', ProcessoViewSet, basename='processo')
router.register(r'auditorias', AuditoriaViewSet, basename='auditoria')
router.register(r'tipos-constatacao', TipoConstatacaoViewSet, basename='tipo-constatacao')
router.register(r'constatacoes', ConstatacaoViewSet, basename='constatacao')
router.register(r'acoes-corretivas', AcaoCorretivaViewSet, basename='acao-corretiva')
router.register(r'documentos', DocumentoAuditoriaViewSet, basename='documento')
router.register(r'comentarios', ComentarioViewSet, basename='comentario')
router.register(r'indicadores', IndicadorAuditoriaViewSet, basename='indicador')

urlpatterns = [
    path('', include(router.urls)),
]
