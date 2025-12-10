import django_filters
from .models import ProgramaAuditoria, Auditoria


class ProgramaAuditoriaFilter(django_filters.FilterSet):
    ano = django_filters.NumberFilter()
    status = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = ProgramaAuditoria
        fields = ['ano', 'status', 'versao']


class AuditoriaFilter(django_filters.FilterSet):
    ano = django_filters.NumberFilter(field_name='programa__ano')
    tipo = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.CharFilter(lookup_expr='iexact')
    auditor = django_filters.NumberFilter(field_name='auditores__id')
    departamento = django_filters.NumberFilter(field_name='departamentos__id')

    class Meta:
        model = Auditoria
        fields = ['programa', 'tipo', 'status']
