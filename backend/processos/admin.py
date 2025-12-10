from django.contrib import admin
from .models import Processo


@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'categoria', 'owner')
    search_fields = ('codigo', 'nome')
    list_filter = ('categoria',)
