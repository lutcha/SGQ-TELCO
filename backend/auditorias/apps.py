from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuditoriasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auditorias'
    verbose_name = _('Módulo de Auditorias')

    def ready(self):
        import auditorias.signals
