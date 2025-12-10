from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Tenant, TipoAuditoria, Processo, Auditoria, TipoConstatacao,
    Constatacao, AcaoCorretiva, DocumentoAuditoria, Comentario, IndicadorAuditoria
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para usuário"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class TenantSerializer(serializers.ModelSerializer):
    """Serializer para Tenant"""
    class Meta:
        model = Tenant
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class TipoAuditoriaSerializer(serializers.ModelSerializer):
    """Serializer para Tipo de Auditoria"""
    class Meta:
        model = TipoAuditoria
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class ProcessoSerializer(serializers.ModelSerializer):
    """Serializer para Processo"""
    responsavel_detalhes = UserSerializer(source='responsavel', read_only=True)
    
    class Meta:
        model = Processo
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class TipoConstatacaoSerializer(serializers.ModelSerializer):
    """Serializer para Tipo de Constatação"""
    severidade_display = serializers.CharField(source='get_severidade_display', read_only=True)
    
    class Meta:
        model = TipoConstatacao
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class AcaoCorretivaSerializer(serializers.ModelSerializer):
    """Serializer para Ação Corretiva"""
    responsavel_detalhes = UserSerializer(source='responsavel', read_only=True)
    verificada_por_detalhes = UserSerializer(source='verificada_por', read_only=True)
    criado_por_detalhes = UserSerializer(source='criado_por', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AcaoCorretiva
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'criado_em', 'atualizado_em', 'criado_por']


class ConstatacaoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Constatações"""
    tipo_detalhes = TipoConstatacaoSerializer(source='tipo', read_only=True)
    processo_detalhes = ProcessoSerializer(source='processo', read_only=True)
    responsavel_detalhes = UserSerializer(source='responsavel', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    dias_em_aberto = serializers.IntegerField(read_only=True)
    total_acoes = serializers.SerializerMethodField()
    
    class Meta:
        model = Constatacao
        fields = [
            'id', 'numero', 'titulo', 'tipo', 'tipo_detalhes', 'processo', 'processo_detalhes',
            'responsavel', 'responsavel_detalhes', 'status', 'status_display', 'prazo_resposta',
            'data_fechamento', 'dias_em_aberto', 'total_acoes', 'criado_em', 'atualizado_em'
        ]
    
    def get_total_acoes(self, obj):
        return obj.acoes_corretivas.count()


class ConstatacaoDetailSerializer(serializers.ModelSerializer):
    """Serializer detalhado para Constatação"""
    tipo_detalhes = TipoConstatacaoSerializer(source='tipo', read_only=True)
    processo_detalhes = ProcessoSerializer(source='processo', read_only=True)
    responsavel_detalhes = UserSerializer(source='responsavel', read_only=True)
    criado_por_detalhes = UserSerializer(source='criado_por', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    dias_em_aberto = serializers.IntegerField(read_only=True)
    acoes_corretivas = AcaoCorretivaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Constatacao
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'criado_em', 'atualizado_em', 'criado_por']


class DocumentoAuditoriaSerializer(serializers.ModelSerializer):
    """Serializer para Documento de Auditoria"""
    enviado_por_detalhes = UserSerializer(source='enviado_por', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = DocumentoAuditoria
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'enviado_em', 'enviado_por']


class ComentarioSerializer(serializers.ModelSerializer):
    """Serializer para Comentário"""
    autor_detalhes = UserSerializer(source='autor', read_only=True)
    
    class Meta:
        model = Comentario
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'criado_em', 'atualizado_em', 'autor']


class AuditoriaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de Auditorias"""
    tipo_detalhes = TipoAuditoriaSerializer(source='tipo', read_only=True)
    auditor_lider_detalhes = UserSerializer(source='auditor_lider', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_constatacoes = serializers.IntegerField(read_only=True)
    constatacoes_abertas = serializers.IntegerField(read_only=True)
    constatacoes_fechadas = serializers.IntegerField(read_only=True)
    total_processos = serializers.SerializerMethodField()
    
    class Meta:
        model = Auditoria
        fields = [
            'id', 'codigo', 'titulo', 'tipo', 'tipo_detalhes', 'status', 'status_display',
            'data_planejada_inicio', 'data_planejada_fim', 'data_real_inicio', 'data_real_fim',
            'auditor_lider', 'auditor_lider_detalhes', 'total_constatacoes', 'constatacoes_abertas',
            'constatacoes_fechadas', 'total_processos', 'criado_em', 'atualizado_em'
        ]
    
    def get_total_processos(self, obj):
        return obj.processos.count()


class AuditoriaDetailSerializer(serializers.ModelSerializer):
    """Serializer detalhado para Auditoria"""
    tipo_detalhes = TipoAuditoriaSerializer(source='tipo', read_only=True)
    processos_detalhes = ProcessoSerializer(source='processos', many=True, read_only=True)
    auditor_lider_detalhes = UserSerializer(source='auditor_lider', read_only=True)
    equipe_auditores_detalhes = UserSerializer(source='equipe_auditores', many=True, read_only=True)
    criado_por_detalhes = UserSerializer(source='criado_por', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    constatacoes = ConstatacaoListSerializer(many=True, read_only=True)
    documentos = DocumentoAuditoriaSerializer(many=True, read_only=True)
    comentarios = ComentarioSerializer(many=True, read_only=True)
    total_constatacoes = serializers.IntegerField(read_only=True)
    constatacoes_abertas = serializers.IntegerField(read_only=True)
    constatacoes_fechadas = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Auditoria
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'criado_em', 'atualizado_em', 'criado_por']


class AuditoriaCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para criação e atualização de Auditoria"""
    
    class Meta:
        model = Auditoria
        exclude = ['tenant', 'criado_por', 'criado_em', 'atualizado_em']
    
    def validate(self, data):
        """Validações customizadas"""
        if data.get('data_planejada_fim') and data.get('data_planejada_inicio'):
            if data['data_planejada_fim'] < data['data_planejada_inicio']:
                raise serializers.ValidationError({
                    'data_planejada_fim': 'A data de fim deve ser posterior à data de início'
                })
        
        if data.get('data_real_fim') and data.get('data_real_inicio'):
            if data['data_real_fim'] < data['data_real_inicio']:
                raise serializers.ValidationError({
                    'data_real_fim': 'A data real de fim deve ser posterior à data real de início'
                })
        
        return data


class IndicadorAuditoriaSerializer(serializers.ModelSerializer):
    """Serializer para Indicador de Auditoria"""
    class Meta:
        model = IndicadorAuditoria
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


# Serializers para Estatísticas e Dashboards
class EstatisticasAuditoriaSerializer(serializers.Serializer):
    """Serializer para estatísticas de auditoria"""
    total_auditorias = serializers.IntegerField()
    auditorias_planejadas = serializers.IntegerField()
    auditorias_em_andamento = serializers.IntegerField()
    auditorias_concluidas = serializers.IntegerField()
    total_constatacoes = serializers.IntegerField()
    constatacoes_abertas = serializers.IntegerField()
    constatacoes_fechadas = serializers.IntegerField()
    taxa_fechamento = serializers.DecimalField(max_digits=5, decimal_places=2)
    constatacoes_criticas = serializers.IntegerField()
    constatacoes_altas = serializers.IntegerField()
    acoes_atrasadas = serializers.IntegerField()


class AuditoriasPorMesSerializer(serializers.Serializer):
    """Serializer para auditorias por mês"""
    mes = serializers.DateField()
    total = serializers.IntegerField()


class ConstatacoesPorTipoSerializer(serializers.Serializer):
    """Serializer para constatações por tipo"""
    tipo = serializers.CharField()
    total = serializers.IntegerField()
    cor = serializers.CharField()
