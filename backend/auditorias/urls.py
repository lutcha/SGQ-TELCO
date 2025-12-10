from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import AuditoriaViewSet, ProgramaAuditoriaViewSet

router = DefaultRouter()
router.register(r'auditorias/programas', ProgramaAuditoriaViewSet, basename='programa-auditoria')
router.register(r'auditorias', AuditoriaViewSet, basename='auditoria')

urlpatterns = [
    path('', include(router.urls)),
]
