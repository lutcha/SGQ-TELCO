from django.contrib.auth import get_user_model
from rest_framework import serializers

from processos.models import Processo
from utilizadores.models import Departamento
from nonconformidades.models import NaoConformidade
from .models import (
    ProgramaAuditoria,
    Auditoria,
    PlanoAuditoria,
    ChecklistAuditoria,
    ItemChecklist,
    Constatacao,
    RelatorioAuditoria,
    SeguimentoAuditoria,
)

User = get_user_model()


class UserSummarySerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'perfil', 'nome']

    def get_nome(self, obj):
        full = f"{obj.first_name} {obj.last_name}".strip()
        return full or obj.username


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'nome', 'sigla']


class ProcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processo
        fields = ['id', 'codigo', 'nome']


class ProgramaAuditoriaSerializer(serializers.ModelSerializer):
    elaborado_por = UserSummarySerializer(read_only=True)
    aprovado_por = UserSummarySerializer(read_only=True)
    elaborado_por_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='elaborado_por', write_only=True
    )
    aprovado_por_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='aprovado_por', allow_null=True, required=False, write_only=True
    )
    total_auditorias = serializers.SerializerMethodField()
    auditorias_concluidas = serializers.SerializerMethodField()

    class Meta:
        model = ProgramaAuditoria
        fields = [
            'id',
            'ano',
            'versao',
            'data_elaboracao',
            'data_aprovacao',
            'status',
            'observacoes',
            'elaborado_por',
            'aprovado_por',
            'elaborado_por_id',
            'aprovado_por_id',
            'total_auditorias',
            'auditorias_concluidas',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

    def get_total_auditorias(self, obj):
        return obj.auditorias.count()

    def get_auditorias_concluidas(self, obj):
        return obj.auditorias.filter(status='CONCLUIDA').count()


class AuditoriaSerializer(serializers.ModelSerializer):
    programa = ProgramaAuditoriaSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgramaAuditoria.objects.all(), source='programa', write_only=True
    )
    processos = serializers.PrimaryKeyRelatedField(many=True, queryset=Processo.objects.all())
    departamentos = serializers.PrimaryKeyRelatedField(many=True, queryset=Departamento.objects.all())
    auditor_lider = UserSummarySerializer(read_only=True)
    auditor_lider_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='auditor_lider', write_only=True
    )
    auditores = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    criado_por = UserSummarySerializer(read_only=True)

    class Meta:
        model = Auditoria
        fields = [
            'id',
            'programa',
            'programa_id',
            'numero_sequencial',
            'tipo',
            'ambito',
            'data_prevista_inicio',
            'data_prevista_fim',
            'data_real_inicio',
            'data_real_fim',
            'processos',
            'departamentos',
            'auditor_lider',
            'auditor_lider_id',
            'auditores',
            'status',
            'total_constatacoes',
            'nao_conformidades_encontradas',
            'oportunidades_melhoria',
            'criado_por',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em', 'criado_por']


class PlanoAuditoriaSerializer(serializers.ModelSerializer):
    elaborado_por = UserSummarySerializer(read_only=True)
    elaborado_por_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='elaborado_por', write_only=True
    )
    aprovado_por = UserSummarySerializer(read_only=True)
    aprovado_por_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='aprovado_por', allow_null=True, required=False, write_only=True
    )

    class Meta:
        model = PlanoAuditoria
        fields = [
            'id',
            'auditoria',
            'normas_referencia',
            'processos_detalhados',
            'metodologia',
            'criterios_auditoria',
            'cronograma',
            'recursos_necessarios',
            'elaborado_por',
            'elaborado_por_id',
            'data_elaboracao',
            'aprovado_por',
            'aprovado_por_id',
            'data_aprovacao',
        ]
        read_only_fields = ['auditoria']


class ItemChecklistSerializer(serializers.ModelSerializer):
    avaliado_por = UserSummarySerializer(read_only=True)
    avaliado_por_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
        source='avaliado_por',
    )

    class Meta:
        model = ItemChecklist
        fields = [
            'id',
            'checklist',
            'numero',
            'requisito',
            'questao',
            'status',
            'observacao',
            'evidencia',
            'avaliado_por',
            'avaliado_por_id',
            'data_avaliacao',
            'ordem',
        ]
        read_only_fields = ['checklist', 'data_avaliacao']


class ChecklistAuditoriaSerializer(serializers.ModelSerializer):
    itens = ItemChecklistSerializer(many=True, read_only=True)
    processo = ProcessoSerializer(read_only=True)
    processo_id = serializers.PrimaryKeyRelatedField(
        queryset=Processo.objects.all(), allow_null=True, required=False, source='processo', write_only=True
    )
    departamento = DepartamentoSerializer(read_only=True)
    departamento_id = serializers.PrimaryKeyRelatedField(
        queryset=Departamento.objects.all(), source='departamento', write_only=True
    )

    class Meta:
        model = ChecklistAuditoria
        fields = [
            'id',
            'auditoria',
            'processo',
            'processo_id',
            'departamento',
            'departamento_id',
            'titulo',
            'descricao',
            'ordem',
            'criado_em',
            'itens',
        ]
        read_only_fields = ['auditoria', 'criado_em']


class ConstatacaoSerializer(serializers.ModelSerializer):
    processo = ProcessoSerializer(read_only=True)
    processo_id = serializers.PrimaryKeyRelatedField(
        queryset=Processo.objects.all(), allow_null=True, required=False, source='processo', write_only=True
    )
    departamento = DepartamentoSerializer(read_only=True)
    departamento_id = serializers.PrimaryKeyRelatedField(
        queryset=Departamento.objects.all(), source='departamento', write_only=True
    )
    item_checklist = serializers.PrimaryKeyRelatedField(
        queryset=ItemChecklist.objects.all(), allow_null=True, required=False
    )
    nao_conformidade = serializers.PrimaryKeyRelatedField(
        queryset=NaoConformidade.objects.all(), allow_null=True, required=False
    )
    identificada_por = UserSummarySerializer(read_only=True)
    identificada_por_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='identificada_por', write_only=True
    )

    class Meta:
        model = Constatacao
        fields = [
            'id',
            'auditoria',
            'item_checklist',
            'numero',
            'tipo',
            'criticidade',
            'processo',
            'processo_id',
            'departamento',
            'departamento_id',
            'requisito_referencia',
            'descricao',
            'evidencia',
            'causa_possivel',
            'nao_conformidade',
            'identificada_por',
            'identificada_por_id',
            'data_identificacao',
        ]
        read_only_fields = ['auditoria', 'data_identificacao']


class RelatorioAuditoriaSerializer(serializers.ModelSerializer):
    elaborado_por = UserSummarySerializer(read_only=True)
    elaborado_por_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='elaborado_por', write_only=True
    )
    aprovado_por = UserSummarySerializer(read_only=True)
    aprovado_por_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='aprovado_por', allow_null=True, required=False, write_only=True
    )

    class Meta:
        model = RelatorioAuditoria
        fields = '__all__'
        read_only_fields = ['auditoria', 'arquivo_pdf']


class SeguimentoAuditoriaSerializer(serializers.ModelSerializer):
    responsavel_seguimento = UserSummarySerializer(read_only=True)
    responsavel_seguimento_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='responsavel_seguimento', write_only=True
    )

    class Meta:
        model = SeguimentoAuditoria
        fields = [
            'id',
            'auditoria',
            'plano_acoes',
            'responsavel_seguimento',
            'responsavel_seguimento_id',
            'acoes_planejadas',
            'acoes_implementadas',
            'acoes_pendentes',
            'acoes_atrasadas',
            'prazo_implementacao',
            'data_verificacao',
            'status',
            'observacoes',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['auditoria', 'criado_em', 'atualizado_em']


class AuditoriaDetailSerializer(AuditoriaSerializer):
    plano = PlanoAuditoriaSerializer(read_only=True)
    checklists = ChecklistAuditoriaSerializer(many=True, read_only=True)
    constatacoes = ConstatacaoSerializer(many=True, read_only=True)
    relatorio = RelatorioAuditoriaSerializer(read_only=True)
    seguimento = SeguimentoAuditoriaSerializer(read_only=True)

    class Meta(AuditoriaSerializer.Meta):
        fields = AuditoriaSerializer.Meta.fields + [
            'plano',
            'checklists',
            'constatacoes',
            'relatorio',
            'seguimento',
        ]


class AuditoriaKpiSerializer(serializers.Serializer):
    auditorias_planeadas = serializers.IntegerField()
    auditorias_realizadas = serializers.IntegerField()
    percentual_execucao = serializers.FloatField()
    tempo_medio_execucao = serializers.FloatField()
    constatacoes_por_auditoria = serializers.FloatField()
    taxa_nc_por_processo = serializers.ListField()
    acoes_corretivas_prazo = serializers.FloatField()
    tempo_fecho_nc = serializers.FloatField()
    evolucao_conformidade = serializers.ListField()
    top_processos_nc = serializers.ListField()
    top_departamentos_om = serializers.ListField()
    taxa_eficacia = serializers.FloatField()


class DashboardResponseSerializer(serializers.Serializer):
    kpis = AuditoriaKpiSerializer()
    auditorias_por_status = serializers.DictField(child=serializers.IntegerField())
    timeline = serializers.ListField()
    mapa_calor = serializers.ListField()
    programa = serializers.DictField()
    constatacoes = serializers.DictField()
    seguimento = serializers.DictField()
