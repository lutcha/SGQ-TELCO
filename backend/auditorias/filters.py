from django_filters import rest_framework as filters
from .models import Auditoria, Constatacao, AcaoCorretiva


class AuditoriaFilter(filters.FilterSet):
    """Filtros customizados para Auditoria"""
    data_inicio = filters.DateFilter(field_name='data_planejada_inicio', lookup_expr='gte')
    data_fim = filters.DateFilter(field_name='data_planejada_fim', lookup_expr='lte')
    ano = filters.NumberFilter(field_name='data_planejada_inicio__year')
    mes = filters.NumberFilter(field_name='data_planejada_inicio__month')
    
    class Meta:
        model = Auditoria
        fields = ['status', 'tipo', 'auditor_lider', 'ano', 'mes']


class ConstatacaoFilter(filters.FilterSet):
    """Filtros customizados para Constatação"""
    prazo_vencido = filters.BooleanFilter(method='filter_prazo_vencido')
    severidade = filters.NumberFilter(field_name='tipo__severidade')
    
    class Meta:
        model = Constatacao
        fields = ['status', 'tipo', 'processo', 'auditoria', 'responsavel']
    
    def filter_prazo_vencido(self, queryset, name, value):
        from django.utils import timezone
        hoje = timezone.now().date()
        
        if value:
            return queryset.filter(
                status__in=['aberta', 'em_tratamento'],
                prazo_resposta__lt=hoje
            )
        return queryset


class AcaoCorretivaFilter(filters.FilterSet):
    """Filtros customizados para Ação Corretiva"""
    atrasada = filters.BooleanFilter(method='filter_atrasada')
    
    class Meta:
        model = AcaoCorretiva
        fields = ['status', 'tipo', 'constatacao', 'responsavel', 'eficaz']
    
    def filter_atrasada(self, queryset, name, value):
        from django.utils import timezone
        hoje = timezone.now().date()
        
        if value:
            return queryset.filter(
                status__in=['planejada', 'em_andamento'],
                prazo_conclusao__lt=hoje
            )
        return queryset
