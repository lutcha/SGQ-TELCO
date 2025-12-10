from django.conf import settings
from django.db import models


class Processo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='processos_responsavel',
    )
    categoria = models.CharField(max_length=120, blank=True)
    kpi_conformidade = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome}"
