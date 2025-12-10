from django.conf import settings
from django.db import models


class ProgramaAuditoriaStatus(models.TextChoices):
    RASCUNHO = 'RASCUNHO', 'Rascunho'
    APROVADO = 'APROVADO', 'Aprovado'
    EM_EXECUCAO = 'EM_EXECUCAO', 'Em Execução'
    CONCLUIDO = 'CONCLUIDO', 'Concluído'


class AuditoriaTipo(models.TextChoices):
    INTERNA_GLOBAL = 'INTERNA_GLOBAL', 'Auditoria Interna Global'
    INTERNA_PARCIAL = 'INTERNA_PARCIAL', 'Auditoria Interna Parcial'
    EXTERNA = 'EXTERNA', 'Auditoria Externa'
    FORNECEDOR = 'FORNECEDOR', 'Auditoria a Fornecedor'


class AuditoriaStatus(models.TextChoices):
    PLANEADA = 'PLANEADA', 'Planeada'
    PREPARACAO = 'PREPARACAO', 'Em Preparação'
    EM_EXECUCAO = 'EM_EXECUCAO', 'Em Execução'
    RELATORIO = 'RELATORIO', 'Elaboração Relatório'
    CONCLUIDA = 'CONCLUIDA', 'Concluída'
    CANCELADA = 'CANCELADA', 'Cancelada'


class ItemChecklistStatus(models.TextChoices):
    PENDENTE = 'PENDENTE', 'Pendente'
    CONFORME = 'CONFORME', 'Conforme'
    NAO_CONFORME = 'NAO_CONFORME', 'Não Conforme'
    NAO_APLICAVEL = 'NAO_APLICAVEL', 'Não Aplicável'
    OPORTUNIDADE = 'OPORTUNIDADE', 'Oportunidade de Melhoria'


class ConstatacaoTipo(models.TextChoices):
    NAO_CONFORMIDADE = 'NAO_CONFORMIDADE', 'Não Conformidade'
    OPORTUNIDADE_MELHORIA = 'OPORTUNIDADE_MELHORIA', 'Oportunidade de Melhoria'
    OBSERVACAO = 'OBSERVACAO', 'Observação'
    PONTO_FORTE = 'PONTO_FORTE', 'Ponto Forte'


class Criticidade(models.TextChoices):
    CRITICA = 'CRITICA', 'Crítica'
    MAIOR = 'MAIOR', 'Maior'
    MENOR = 'MENOR', 'Menor'


class SeguimentoStatus(models.TextChoices):
    EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em Andamento'
    CONCLUIDO = 'CONCLUIDO', 'Concluído'
    ATRASADO = 'ATRASADO', 'Atrasado'


class ProgramaAuditoria(models.Model):
    """Programa Anual de Auditorias"""

    ano = models.IntegerField()
    versao = models.CharField(max_length=10)
    data_elaboracao = models.DateField()
    data_aprovacao = models.DateField(null=True, blank=True)

    elaborado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='programas_elaborados',
        on_delete=models.PROTECT,
    )
    aprovado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='programas_aprovados',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ProgramaAuditoriaStatus.choices,
        default=ProgramaAuditoriaStatus.RASCUNHO,
    )

    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ano', '-versao']
        unique_together = ('ano', 'versao')
        verbose_name = 'Programa de Auditoria'
        verbose_name_plural = 'Programas de Auditoria'

    def __str__(self) -> str:
        return f"Programa {self.ano}/{self.versao}"


class Auditoria(models.Model):
    """Auditoria Individual"""

    programa = models.ForeignKey(
        ProgramaAuditoria,
        related_name='auditorias',
        on_delete=models.CASCADE,
    )
    numero_sequencial = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=20, choices=AuditoriaTipo.choices)
    ambito = models.TextField(help_text='Processos/áreas a auditar')

    data_prevista_inicio = models.DateField()
    data_prevista_fim = models.DateField()
    data_real_inicio = models.DateField(null=True, blank=True)
    data_real_fim = models.DateField(null=True, blank=True)

    processos = models.ManyToManyField(
        'processos.Processo',
        related_name='auditorias',
        blank=True,
    )
    departamentos = models.ManyToManyField(
        'utilizadores.Departamento',
        related_name='auditorias',
        blank=True,
    )

    auditor_lider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='auditorias_lideradas',
        on_delete=models.PROTECT,
    )
    auditores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='auditorias_participadas',
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=AuditoriaStatus.choices,
        default=AuditoriaStatus.PLANEADA,
    )

    total_constatacoes = models.IntegerField(default=0)
    nao_conformidades_encontradas = models.IntegerField(default=0)
    oportunidades_melhoria = models.IntegerField(default=0)

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='auditorias_criadas',
        on_delete=models.PROTECT,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self) -> str:
        return self.numero_sequencial


class PlanoAuditoria(models.Model):
    """Plano detalhado da auditoria"""

    auditoria = models.OneToOneField(
        Auditoria,
        related_name='plano',
        on_delete=models.CASCADE,
    )
    normas_referencia = models.JSONField(default=list)
    processos_detalhados = models.JSONField(default=list)
    metodologia = models.TextField()
    criterios_auditoria = models.TextField()
    cronograma = models.JSONField(default=list)
    recursos_necessarios = models.TextField(blank=True)
    elaborado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='planos_auditoria_elaborados',
    )
    data_elaboracao = models.DateField()
    aprovado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='planos_auditoria_aprovados',
    )
    data_aprovacao = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Plano de Auditoria'

    def __str__(self) -> str:
        return f"Plano {self.auditoria.numero_sequencial}"


class ChecklistAuditoria(models.Model):
    """Checklist/Questionário de auditoria"""

    auditoria = models.ForeignKey(
        Auditoria,
        related_name='checklists',
        on_delete=models.CASCADE,
    )
    processo = models.ForeignKey(
        'processos.Processo',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    departamento = models.ForeignKey(
        'utilizadores.Departamento',
        on_delete=models.PROTECT,
    )

    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    ordem = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem', 'criado_em']

    def __str__(self) -> str:
        return self.titulo


class ItemChecklist(models.Model):
    """Item individual do checklist"""

    checklist = models.ForeignKey(
        ChecklistAuditoria,
        related_name='itens',
        on_delete=models.CASCADE,
    )
    numero = models.CharField(max_length=20)
    requisito = models.TextField()
    questao = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ItemChecklistStatus.choices,
        default=ItemChecklistStatus.PENDENTE,
    )
    observacao = models.TextField(blank=True)
    evidencia = models.TextField(blank=True)
    avaliado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    data_avaliacao = models.DateTimeField(null=True, blank=True)
    ordem = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordem', 'numero']

    def __str__(self) -> str:
        return f"{self.numero} - {self.questao[:30]}"


class Constatacao(models.Model):
    """Constatação de auditoria"""

    auditoria = models.ForeignKey(
        Auditoria,
        related_name='constatacoes',
        on_delete=models.CASCADE,
    )
    item_checklist = models.ForeignKey(
        ItemChecklist,
        null=True,
        blank=True,
        related_name='constatacoes',
        on_delete=models.SET_NULL,
    )
    numero = models.CharField(max_length=50)
    tipo = models.CharField(max_length=30, choices=ConstatacaoTipo.choices)
    criticidade = models.CharField(
        max_length=10,
        choices=Criticidade.choices,
        null=True,
        blank=True,
    )
    processo = models.ForeignKey(
        'processos.Processo',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    departamento = models.ForeignKey(
        'utilizadores.Departamento',
        on_delete=models.PROTECT,
    )
    requisito_referencia = models.CharField(max_length=100)
    descricao = models.TextField()
    evidencia = models.TextField()
    causa_possivel = models.TextField(blank=True)
    nao_conformidade = models.ForeignKey(
        'nonconformidades.NaoConformidade',
        null=True,
        blank=True,
        related_name='constatacoes_origem',
        on_delete=models.SET_NULL,
    )
    identificada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    data_identificacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_identificacao']

    def __str__(self) -> str:
        return f"Constatação {self.numero}"


class RelatorioAuditoria(models.Model):
    """Relatório final de auditoria"""

    auditoria = models.OneToOneField(
        Auditoria,
        related_name='relatorio',
        on_delete=models.CASCADE,
    )
    resumo_executivo = models.TextField()
    objetivos = models.TextField()
    metodologia = models.TextField()
    ambito_detalhado = models.TextField()
    sintese_resultados = models.TextField()
    pontos_fortes = models.TextField(blank=True)
    areas_melhoria = models.TextField(blank=True)
    total_constatacoes = models.IntegerField()
    nao_conformidades_criticas = models.IntegerField(default=0)
    nao_conformidades_maiores = models.IntegerField(default=0)
    nao_conformidades_menores = models.IntegerField(default=0)
    oportunidades_melhoria = models.IntegerField(default=0)
    conclusoes = models.TextField()
    recomendacoes = models.TextField(blank=True)
    anexos = models.JSONField(default=list)
    elaborado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='relatorios_elaborados',
        on_delete=models.PROTECT,
    )
    data_elaboracao = models.DateField()
    aprovado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='relatorios_aprovados',
        on_delete=models.PROTECT,
    )
    data_aprovacao = models.DateField(null=True, blank=True)
    arquivo_pdf = models.FileField(
        upload_to='auditorias/relatorios/',
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"Relatório {self.auditoria.numero_sequencial}"


class SeguimentoAuditoria(models.Model):
    """Acompanhamento de ações pós-auditoria"""

    auditoria = models.OneToOneField(
        Auditoria,
        related_name='seguimento',
        on_delete=models.CASCADE,
    )
    plano_acoes = models.TextField()
    responsavel_seguimento = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    acoes_planejadas = models.IntegerField()
    acoes_implementadas = models.IntegerField(default=0)
    acoes_pendentes = models.IntegerField()
    acoes_atrasadas = models.IntegerField(default=0)
    prazo_implementacao = models.DateField()
    data_verificacao = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=SeguimentoStatus.choices,
        default=SeguimentoStatus.EM_ANDAMENTO,
    )
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Seguimento {self.auditoria.numero_sequencial}"
