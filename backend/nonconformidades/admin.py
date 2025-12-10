from django.contrib import admin
from .models import NaoConformidade


@admin.register(NaoConformidade)
class NaoConformidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'status', 'processo', 'departamento')
    search_fields = ('codigo', 'titulo')
    list_filter = ('status',)
