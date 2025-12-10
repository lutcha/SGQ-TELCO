from django.conf import settings
from django.db import models


class NaoConformidadeStatus(models.TextChoices):
    ABERTA = 'ABERTA', 'Aberta'
    EM_ANALISE = 'EM_ANALISE', 'Em Análise'
    EM_TRATAMENTO = 'EM_TRATAMENTO', 'Em Tratamento'
    ENCERRADA = 'ENCERRADA', 'Encerrada'


class NaoConformidade(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    processo = models.ForeignKey(
        'processos.Processo',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    departamento = models.ForeignKey(
        'utilizadores.Departamento',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='ncs_responsavel',
    )
    status = models.CharField(
        max_length=20,
        choices=NaoConformidadeStatus.choices,
        default=NaoConformidadeStatus.ABERTA,
    )
    data_abertura = models.DateField()
    data_fecho = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"NC {self.codigo}"
