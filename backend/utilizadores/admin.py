from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Departamento, Utilizador


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'gestor')
    search_fields = ('nome', 'sigla')


@admin.register(Utilizador)
class UtilizadorAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Informações Organizacionais',
            {
                'fields': ('perfil', 'departamento', 'cargo'),
            },
        ),
    )
    list_display = UserAdmin.list_display + ('perfil', 'departamento')
    list_filter = UserAdmin.list_filter + ('perfil', 'departamento')
