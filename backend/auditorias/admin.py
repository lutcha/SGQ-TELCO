from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Tenant, TipoAuditoria, Processo, Auditoria, TipoConstatacao,
    Constatacao, AcaoCorretiva, DocumentoAuditoria, Comentario, IndicadorAuditoria
)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'codigo']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'codigo', 'ativo')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TipoAuditoria)
class TipoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tenant', 'cor_badge', 'ativo', 'criado_em']
    list_filter = ['tenant', 'ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    def cor_badge(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; border-radius: 3px; color: white;">{}</span>',
            obj.cor, obj.nome
        )
    cor_badge.short_description = 'Cor'


@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'responsavel', 'tenant', 'ativo', 'criado_em']
    list_filter = ['tenant', 'ativo', 'criado_em']
    search_fields = ['codigo', 'nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    autocomplete_fields = ['responsavel']


@admin.register(TipoConstatacao)
class TipoConstatacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tenant', 'severidade', 'cor_badge', 'requer_acao', 'ativo']
    list_filter = ['tenant', 'severidade', 'requer_acao', 'ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    def cor_badge(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; border-radius: 3px; color: white;">{}</span>',
            obj.cor, obj.get_severidade_display()
        )
    cor_badge.short_description = 'Severidade'


class ConstatacaoInline(admin.TabularInline):
    model = Constatacao
    extra = 0
    fields = ['numero', 'titulo', 'tipo', 'processo', 'status', 'prazo_resposta']
    readonly_fields = ['numero']
    autocomplete_fields = ['tipo', 'processo', 'responsavel']


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'titulo', 'tipo', 'status_badge', 'auditor_lider', 'data_planejada_inicio', 'total_constatacoes']
    list_filter = ['tenant', 'status', 'tipo', 'data_planejada_inicio', 'criado_em']
    search_fields = ['codigo', 'titulo', 'descricao', 'objetivo', 'escopo']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por', 'total_constatacoes', 'constatacoes_abertas', 'constatacoes_fechadas']
    autocomplete_fields = ['tipo', 'auditor_lider', 'equipe_auditores', 'processos']
    filter_horizontal = ['processos', 'equipe_auditores']
    inlines = [ConstatacaoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tenant', 'codigo', 'titulo', 'tipo', 'descricao')
        }),
        ('Escopo', {
            'fields': ('objetivo', 'escopo', 'processos', 'norma_referencia', 'criterios_auditoria')
        }),
        ('Planejamento', {
            'fields': ('data_planejada_inicio', 'data_planejada_fim', 'data_real_inicio', 'data_real_fim')
        }),
        ('Equipe', {
            'fields': ('auditor_lider', 'equipe_auditores')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Estatísticas', {
            'fields': ('total_constatacoes', 'constatacoes_abertas', 'constatacoes_fechadas'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('criado_por', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'planejada': '#2196F3',
            'em_andamento': '#FF9800',
            'concluida': '#4CAF50',
            'cancelada': '#F44336',
        }
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; border-radius: 3px; color: white;">{}</span>',
            colors.get(obj.status, '#999'), obj.get_status_display()
        )
    status_badge.short_description = 'Status'


class AcaoCorretivaInline(admin.TabularInline):
    model = AcaoCorretiva
    extra = 0
    fields = ['numero', 'tipo', 'descricao', 'responsavel', 'status', 'prazo_conclusao']
    readonly_fields = ['numero']
    autocomplete_fields = ['responsavel']


@admin.register(Constatacao)
class ConstatacaoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'titulo', 'auditoria', 'tipo', 'status_badge', 'responsavel', 'prazo_resposta', 'dias_em_aberto']
    list_filter = ['tenant', 'status', 'tipo', 'auditoria', 'criado_em']
    search_fields = ['numero', 'titulo', 'descricao', 'evidencia']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por', 'dias_em_aberto']
    autocomplete_fields = ['auditoria', 'tipo', 'processo', 'responsavel']
    inlines = [AcaoCorretivaInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tenant', 'auditoria', 'numero', 'titulo', 'tipo', 'processo')
        }),
        ('Descrição', {
            'fields': ('descricao', 'evidencia', 'requisito')
        }),
        ('Responsabilidade e Prazos', {
            'fields': ('responsavel', 'prazo_resposta', 'data_fechamento')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Análise', {
            'fields': ('analise_causa_raiz',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('criado_por', 'criado_em', 'atualizado_em', 'dias_em_aberto'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'aberta': '#F44336',
            'em_tratamento': '#FF9800',
            'aguardando_validacao': '#2196F3',
            'fechada': '#4CAF50',
            'cancelada': '#999',
        }
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; border-radius: 3px; color: white;">{}</span>',
            colors.get(obj.status, '#999'), obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(AcaoCorretiva)
class AcaoCorretivaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'constatacao', 'tipo', 'status_badge', 'responsavel', 'prazo_conclusao', 'eficaz']
    list_filter = ['tenant', 'status', 'tipo', 'eficaz', 'criado_em']
    search_fields = ['numero', 'descricao', 'objetivo']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']
    autocomplete_fields = ['constatacao', 'responsavel', 'verificada_por']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tenant', 'constatacao', 'numero', 'tipo')
        }),
        ('Descrição', {
            'fields': ('descricao', 'objetivo')
        }),
        ('Responsabilidade e Prazos', {
            'fields': ('responsavel', 'prazo_conclusao', 'data_conclusao')
        }),
        ('Status e Execução', {
            'fields': ('status', 'evidencia_execucao')
        }),
        ('Verificação', {
            'fields': ('verificada_por', 'data_verificacao', 'resultado_verificacao', 'eficaz'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('criado_por', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'planejada': '#2196F3',
            'em_andamento': '#FF9800',
            'concluida': '#4CAF50',
            'verificada': '#009688',
            'cancelada': '#999',
        }
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; border-radius: 3px; color: white;">{}</span>',
            colors.get(obj.status, '#999'), obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(DocumentoAuditoria)
class DocumentoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'auditoria', 'constatacao', 'tipo', 'tamanho_formatado', 'enviado_por', 'enviado_em']
    list_filter = ['tenant', 'tipo', 'enviado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['enviado_em', 'enviado_por', 'tamanho']
    autocomplete_fields = ['auditoria', 'constatacao']
    
    def tamanho_formatado(self, obj):
        if obj.tamanho < 1024:
            return f"{obj.tamanho} B"
        elif obj.tamanho < 1024 * 1024:
            return f"{obj.tamanho / 1024:.2f} KB"
        else:
            return f"{obj.tamanho / (1024 * 1024):.2f} MB"
    tamanho_formatado.short_description = 'Tamanho'


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'auditoria', 'constatacao', 'texto_resumo', 'criado_em']
    list_filter = ['tenant', 'criado_em']
    search_fields = ['texto']
    readonly_fields = ['criado_em', 'atualizado_em', 'autor']
    autocomplete_fields = ['auditoria', 'constatacao']
    
    def texto_resumo(self, obj):
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_resumo.short_description = 'Texto'


@admin.register(IndicadorAuditoria)
class IndicadorAuditoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tenant', 'meta', 'unidade', 'ativo', 'criado_em']
    list_filter = ['tenant', 'ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
