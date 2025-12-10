from django.contrib import admin
from . import models


@admin.register(models.ProgramaAuditoria)
class ProgramaAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('ano', 'versao', 'status', 'elaborado_por', 'aprovado_por')
    search_fields = ('ano', 'versao')
    list_filter = ('status',)


@admin.register(models.Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = (
        'numero_sequencial',
        'tipo',
        'status',
        'programa',
        'auditor_lider',
        'criado_em',
    )
    search_fields = ('numero_sequencial', 'ambito')
    list_filter = ('tipo', 'status')
    filter_horizontal = ('processos', 'departamentos', 'auditores')


@admin.register(models.PlanoAuditoria)
class PlanoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('auditoria', 'elaborado_por', 'data_elaboracao', 'aprovado_por')


@admin.register(models.ChecklistAuditoria)
class ChecklistAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'auditoria', 'departamento', 'ordem')
    list_filter = ('departamento',)


@admin.register(models.ItemChecklist)
class ItemChecklistAdmin(admin.ModelAdmin):
    list_display = ('numero', 'checklist', 'status', 'avaliado_por')
    list_filter = ('status',)


@admin.register(models.Constatacao)
class ConstatacaoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'auditoria', 'tipo', 'criticidade', 'departamento')
    list_filter = ('tipo', 'criticidade', 'departamento')


@admin.register(models.RelatorioAuditoria)
class RelatorioAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('auditoria', 'elaborado_por', 'data_elaboracao', 'aprovado_por')


@admin.register(models.SeguimentoAuditoria)
class SeguimentoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('auditoria', 'status', 'responsavel_seguimento', 'prazo_implementacao')
    list_filter = ('status',)
