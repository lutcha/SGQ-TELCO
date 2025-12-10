from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Tenant(models.Model):
    """Modelo para suporte multi-tenant"""
    nome = models.CharField(max_length=200, verbose_name=_("Nome"))
    codigo = models.CharField(max_length=50, unique=True, verbose_name=_("Código"))
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")
        ordering = ['nome']

    def __str__(self):
        return self.nome


class TipoAuditoria(models.Model):
    """Tipos de auditoria: Interna, Externa, de Fornecedor, etc."""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tipos_auditoria')
    nome = models.CharField(max_length=100, verbose_name=_("Nome"))
    descricao = models.TextField(blank=True, verbose_name=_("Descrição"))
    cor = models.CharField(max_length=7, default='#0066cc', verbose_name=_("Cor (Hex)"))
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Tipo de Auditoria")
        verbose_name_plural = _("Tipos de Auditoria")
        ordering = ['nome']
        unique_together = ['tenant', 'nome']

    def __str__(self):
        return f"{self.nome}"


class Processo(models.Model):
    """Processos da organização que podem ser auditados"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='processos')
    codigo = models.CharField(max_length=50, verbose_name=_("Código"))
    nome = models.CharField(max_length=200, verbose_name=_("Nome"))
    descricao = models.TextField(blank=True, verbose_name=_("Descrição"))
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='processos_responsavel', verbose_name=_("Responsável"))
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Processo")
        verbose_name_plural = _("Processos")
        ordering = ['codigo']
        unique_together = ['tenant', 'codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Auditoria(models.Model):
    """Auditoria principal"""
    
    STATUS_CHOICES = [
        ('planejada', _('Planejada')),
        ('em_andamento', _('Em Andamento')),
        ('concluida', _('Concluída')),
        ('cancelada', _('Cancelada')),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='auditorias')
    codigo = models.CharField(max_length=50, verbose_name=_("Código"))
    titulo = models.CharField(max_length=200, verbose_name=_("Título"))
    tipo = models.ForeignKey(TipoAuditoria, on_delete=models.PROTECT, related_name='auditorias', 
                            verbose_name=_("Tipo"))
    descricao = models.TextField(blank=True, verbose_name=_("Descrição"))
    objetivo = models.TextField(verbose_name=_("Objetivo"))
    escopo = models.TextField(verbose_name=_("Escopo"))
    
    # Datas
    data_planejada_inicio = models.DateField(verbose_name=_("Data Planejada de Início"))
    data_planejada_fim = models.DateField(verbose_name=_("Data Planejada de Fim"))
    data_real_inicio = models.DateField(null=True, blank=True, verbose_name=_("Data Real de Início"))
    data_real_fim = models.DateField(null=True, blank=True, verbose_name=_("Data Real de Fim"))
    
    # Processos auditados
    processos = models.ManyToManyField(Processo, related_name='auditorias', verbose_name=_("Processos"))
    
    # Equipe
    auditor_lider = models.ForeignKey(User, on_delete=models.PROTECT, related_name='auditorias_lider',
                                     verbose_name=_("Auditor Líder"))
    equipe_auditores = models.ManyToManyField(User, related_name='auditorias_equipe', blank=True,
                                              verbose_name=_("Equipe de Auditores"))
    
    # Status e controle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejada',
                             verbose_name=_("Status"))
    norma_referencia = models.CharField(max_length=200, blank=True, 
                                       verbose_name=_("Norma de Referência"))
    criterios_auditoria = models.TextField(blank=True, verbose_name=_("Critérios de Auditoria"))
    
    # Metadados
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='auditorias_criadas',
                                  verbose_name=_("Criado por"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Auditoria")
        verbose_name_plural = _("Auditorias")
        ordering = ['-data_planejada_inicio', 'codigo']
        unique_together = ['tenant', 'codigo']

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"

    @property
    def total_constatacoes(self):
        return self.constatacoes.count()

    @property
    def constatacoes_abertas(self):
        return self.constatacoes.filter(status='aberta').count()

    @property
    def constatacoes_fechadas(self):
        return self.constatacoes.filter(status='fechada').count()


class TipoConstatacao(models.Model):
    """Tipos de constatação: Não Conformidade Maior, Menor, Observação, Oportunidade de Melhoria"""
    
    SEVERIDADE_CHOICES = [
        (1, _('Baixa')),
        (2, _('Média')),
        (3, _('Alta')),
        (4, _('Crítica')),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tipos_constatacao')
    nome = models.CharField(max_length=100, verbose_name=_("Nome"))
    descricao = models.TextField(blank=True, verbose_name=_("Descrição"))
    severidade = models.IntegerField(choices=SEVERIDADE_CHOICES, default=2, verbose_name=_("Severidade"))
    cor = models.CharField(max_length=7, default='#ff9800', verbose_name=_("Cor (Hex)"))
    requer_acao = models.BooleanField(default=True, verbose_name=_("Requer Ação Corretiva"))
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Tipo de Constatação")
        verbose_name_plural = _("Tipos de Constatação")
        ordering = ['-severidade', 'nome']
        unique_together = ['tenant', 'nome']

    def __str__(self):
        return f"{self.nome}"


class Constatacao(models.Model):
    """Constatações/Achados de auditoria (findings)"""
    
    STATUS_CHOICES = [
        ('aberta', _('Aberta')),
        ('em_tratamento', _('Em Tratamento')),
        ('aguardando_validacao', _('Aguardando Validação')),
        ('fechada', _('Fechada')),
        ('cancelada', _('Cancelada')),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='constatacoes')
    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, related_name='constatacoes',
                                 verbose_name=_("Auditoria"))
    numero = models.CharField(max_length=50, verbose_name=_("Número"))
    tipo = models.ForeignKey(TipoConstatacao, on_delete=models.PROTECT, related_name='constatacoes',
                            verbose_name=_("Tipo"))
    processo = models.ForeignKey(Processo, on_delete=models.PROTECT, related_name='constatacoes',
                                verbose_name=_("Processo"))
    
    # Descrição da constatação
    titulo = models.CharField(max_length=200, verbose_name=_("Título"))
    descricao = models.TextField(verbose_name=_("Descrição"))
    evidencia = models.TextField(verbose_name=_("Evidência"))
    requisito = models.CharField(max_length=200, blank=True, verbose_name=_("Requisito da Norma"))
    
    # Responsabilidade
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT, related_name='constatacoes_responsavel',
                                   verbose_name=_("Responsável"))
    
    # Prazos
    prazo_resposta = models.DateField(verbose_name=_("Prazo para Resposta"))
    data_fechamento = models.DateField(null=True, blank=True, verbose_name=_("Data de Fechamento"))
    
    # Status
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='aberta',
                             verbose_name=_("Status"))
    
    # Análise de causa raiz
    analise_causa_raiz = models.TextField(blank=True, verbose_name=_("Análise de Causa Raiz"))
    
    # Metadados
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='constatacoes_criadas',
                                  verbose_name=_("Criado por"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Constatação")
        verbose_name_plural = _("Constatações")
        ordering = ['-criado_em', 'numero']
        unique_together = ['tenant', 'numero']

    def __str__(self):
        return f"{self.numero} - {self.titulo}"

    @property
    def dias_em_aberto(self):
        if self.status in ['fechada', 'cancelada']:
            return 0
        from django.utils import timezone
        return (timezone.now().date() - self.criado_em.date()).days


class AcaoCorretiva(models.Model):
    """Ações corretivas para tratar constatações"""
    
    STATUS_CHOICES = [
        ('planejada', _('Planejada')),
        ('em_andamento', _('Em Andamento')),
        ('concluida', _('Concluída')),
        ('verificada', _('Verificada')),
        ('cancelada', _('Cancelada')),
    ]
    
    TIPO_CHOICES = [
        ('imediata', _('Ação Imediata')),
        ('corretiva', _('Ação Corretiva')),
        ('preventiva', _('Ação Preventiva')),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='acoes_corretivas')
    constatacao = models.ForeignKey(Constatacao, on_delete=models.CASCADE, related_name='acoes_corretivas',
                                   verbose_name=_("Constatação"))
    numero = models.CharField(max_length=50, verbose_name=_("Número"))
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name=_("Tipo"))
    
    # Descrição
    descricao = models.TextField(verbose_name=_("Descrição da Ação"))
    objetivo = models.TextField(verbose_name=_("Objetivo"))
    
    # Responsabilidade e prazos
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT, related_name='acoes_responsavel',
                                   verbose_name=_("Responsável"))
    prazo_conclusao = models.DateField(verbose_name=_("Prazo de Conclusão"))
    data_conclusao = models.DateField(null=True, blank=True, verbose_name=_("Data de Conclusão"))
    
    # Execução
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejada',
                             verbose_name=_("Status"))
    evidencia_execucao = models.TextField(blank=True, verbose_name=_("Evidência de Execução"))
    
    # Verificação
    verificada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='acoes_verificadas', verbose_name=_("Verificada por"))
    data_verificacao = models.DateField(null=True, blank=True, verbose_name=_("Data de Verificação"))
    resultado_verificacao = models.TextField(blank=True, verbose_name=_("Resultado da Verificação"))
    eficaz = models.BooleanField(null=True, blank=True, verbose_name=_("Eficaz"))
    
    # Metadados
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='acoes_criadas',
                                  verbose_name=_("Criado por"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Ação Corretiva")
        verbose_name_plural = _("Ações Corretivas")
        ordering = ['-criado_em', 'numero']
        unique_together = ['tenant', 'numero']

    def __str__(self):
        return f"{self.numero} - {self.descricao[:50]}"


class DocumentoAuditoria(models.Model):
    """Documentos anexados à auditoria"""
    
    TIPO_CHOICES = [
        ('plano', _('Plano de Auditoria')),
        ('checklist', _('Checklist')),
        ('evidencia', _('Evidência')),
        ('relatorio', _('Relatório')),
        ('outro', _('Outro')),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='documentos_auditoria')
    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, related_name='documentos',
                                 verbose_name=_("Auditoria"))
    constatacao = models.ForeignKey(Constatacao, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='documentos', verbose_name=_("Constatação"))
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name=_("Tipo"))
    nome = models.CharField(max_length=200, verbose_name=_("Nome"))
    descricao = models.TextField(blank=True, verbose_name=_("Descrição"))
    arquivo = models.FileField(upload_to='auditorias/documentos/%Y/%m/', verbose_name=_("Arquivo"))
    tamanho = models.IntegerField(verbose_name=_("Tamanho (bytes)"))
    
    # Metadados
    enviado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='documentos_enviados',
                                   verbose_name=_("Enviado por"))
    enviado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Enviado em"))

    class Meta:
        verbose_name = _("Documento de Auditoria")
        verbose_name_plural = _("Documentos de Auditoria")
        ordering = ['-enviado_em']

    def __str__(self):
        return self.nome


class Comentario(models.Model):
    """Comentários em auditorias e constatações"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='comentarios')
    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='comentarios', verbose_name=_("Auditoria"))
    constatacao = models.ForeignKey(Constatacao, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='comentarios', verbose_name=_("Constatação"))
    
    texto = models.TextField(verbose_name=_("Texto"))
    
    # Metadados
    autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comentarios_autor',
                             verbose_name=_("Autor"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Comentário")
        verbose_name_plural = _("Comentários")
        ordering = ['criado_em']

    def __str__(self):
        return f"Comentário por {self.autor} em {self.criado_em}"


class IndicadorAuditoria(models.Model):
    """Indicadores e métricas de auditoria"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='indicadores')
    nome = models.CharField(max_length=200, verbose_name=_("Nome"))
    descricao = models.TextField(blank=True, verbose_name=_("Descrição"))
    formula = models.TextField(verbose_name=_("Fórmula de Cálculo"))
    meta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Meta"))
    unidade = models.CharField(max_length=50, verbose_name=_("Unidade"))
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Indicador de Auditoria")
        verbose_name_plural = _("Indicadores de Auditoria")
        ordering = ['nome']

    def __str__(self):
        return self.nome
