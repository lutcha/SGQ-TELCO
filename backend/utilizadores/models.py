from django.contrib.auth.models import AbstractUser
from django.db import models


class PerfilChoices(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    DIRETOR = 'DIRETOR', 'Diretor'
    PROCESS_OWNER = 'PROCESS_OWNER', 'Process Owner'
    GESTOR = 'GESTOR', 'Gestor Qualidade'
    AUDITOR = 'AUDITOR', 'Auditor Interno'
    COLABORADOR = 'COLABORADOR', 'Colaborador'


class Departamento(models.Model):
    nome = models.CharField(max_length=120)
    sigla = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True)
    gestor = models.ForeignKey(
        'utilizadores.Utilizador',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='departamentos_geridos',
    )

    def __str__(self) -> str:
        return self.nome


class Utilizador(AbstractUser):
    perfil = models.CharField(
        max_length=20,
        choices=PerfilChoices.choices,
        default=PerfilChoices.COLABORADOR,
    )
    departamento = models.ForeignKey(
        Departamento,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='membros',
    )
    cargo = models.CharField(max_length=120, blank=True)

    def __str__(self) -> str:
        return f"{self.get_full_name() or self.username}"
