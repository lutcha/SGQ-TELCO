from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import (
    Tenant, TipoAuditoria, Processo, Auditoria, TipoConstatacao,
    Constatacao, AcaoCorretiva
)

User = get_user_model()


class TenantModelTest(TestCase):
    """Testes para o modelo Tenant"""
    
    def setUp(self):
        self.tenant = Tenant.objects.create(
            nome="Empresa Teste",
            codigo="EMP001"
        )
    
    def test_tenant_criacao(self):
        """Testar criação de tenant"""
        self.assertEqual(self.tenant.nome, "Empresa Teste")
        self.assertEqual(self.tenant.codigo, "EMP001")
        self.assertTrue(self.tenant.ativo)
    
    def test_tenant_str(self):
        """Testar representação string do tenant"""
        self.assertEqual(str(self.tenant), "Empresa Teste")


class AuditoriaModelTest(TestCase):
    """Testes para o modelo Auditoria"""
    
    def setUp(self):
        self.tenant = Tenant.objects.create(nome="Empresa Teste", codigo="EMP001")
        self.user = User.objects.create_user(username="auditor", email="auditor@test.com")
        self.tipo = TipoAuditoria.objects.create(
            tenant=self.tenant,
            nome="Auditoria Interna"
        )
        self.processo = Processo.objects.create(
            tenant=self.tenant,
            codigo="PROC001",
            nome="Processo Teste"
        )
        self.auditoria = Auditoria.objects.create(
            tenant=self.tenant,
            codigo="AUD-2024-0001",
            titulo="Auditoria de Teste",
            tipo=self.tipo,
            objetivo="Objetivo da auditoria",
            escopo="Escopo da auditoria",
            data_planejada_inicio=timezone.now().date(),
            data_planejada_fim=timezone.now().date() + timedelta(days=7),
            auditor_lider=self.user,
            criado_por=self.user
        )
        self.auditoria.processos.add(self.processo)
    
    def test_auditoria_criacao(self):
        """Testar criação de auditoria"""
        self.assertEqual(self.auditoria.codigo, "AUD-2024-0001")
        self.assertEqual(self.auditoria.titulo, "Auditoria de Teste")
        self.assertEqual(self.auditoria.status, "planejada")
    
    def test_auditoria_str(self):
        """Testar representação string da auditoria"""
        self.assertEqual(str(self.auditoria), "AUD-2024-0001 - Auditoria de Teste")
    
    def test_auditoria_total_constatacoes(self):
        """Testar contagem de constatações"""
        self.assertEqual(self.auditoria.total_constatacoes, 0)


class ConstatacaoModelTest(TestCase):
    """Testes para o modelo Constatação"""
    
    def setUp(self):
        self.tenant = Tenant.objects.create(nome="Empresa Teste", codigo="EMP001")
        self.user = User.objects.create_user(username="auditor", email="auditor@test.com")
        self.tipo_auditoria = TipoAuditoria.objects.create(
            tenant=self.tenant,
            nome="Auditoria Interna"
        )
        self.tipo_constatacao = TipoConstatacao.objects.create(
            tenant=self.tenant,
            nome="Não Conformidade Menor",
            severidade=2
        )
        self.processo = Processo.objects.create(
            tenant=self.tenant,
            codigo="PROC001",
            nome="Processo Teste"
        )
        self.auditoria = Auditoria.objects.create(
            tenant=self.tenant,
            codigo="AUD-2024-0001",
            titulo="Auditoria de Teste",
            tipo=self.tipo_auditoria,
            objetivo="Objetivo",
            escopo="Escopo",
            data_planejada_inicio=timezone.now().date(),
            data_planejada_fim=timezone.now().date() + timedelta(days=7),
            auditor_lider=self.user,
            criado_por=self.user
        )
        self.constatacao = Constatacao.objects.create(
            tenant=self.tenant,
            auditoria=self.auditoria,
            numero="CONST-2024-0001",
            tipo=self.tipo_constatacao,
            processo=self.processo,
            titulo="Constatação Teste",
            descricao="Descrição da constatação",
            evidencia="Evidência da constatação",
            responsavel=self.user,
            prazo_resposta=timezone.now().date() + timedelta(days=30),
            criado_por=self.user
        )
    
    def test_constatacao_criacao(self):
        """Testar criação de constatação"""
        self.assertEqual(self.constatacao.numero, "CONST-2024-0001")
        self.assertEqual(self.constatacao.titulo, "Constatação Teste")
        self.assertEqual(self.constatacao.status, "aberta")
    
    def test_constatacao_str(self):
        """Testar representação string da constatação"""
        self.assertEqual(str(self.constatacao), "CONST-2024-0001 - Constatação Teste")
    
    def test_constatacao_dias_em_aberto(self):
        """Testar cálculo de dias em aberto"""
        self.assertGreaterEqual(self.constatacao.dias_em_aberto, 0)


class AcaoCorretivaModelTest(TestCase):
    """Testes para o modelo Ação Corretiva"""
    
    def setUp(self):
        self.tenant = Tenant.objects.create(nome="Empresa Teste", codigo="EMP001")
        self.user = User.objects.create_user(username="auditor", email="auditor@test.com")
        self.tipo_auditoria = TipoAuditoria.objects.create(
            tenant=self.tenant,
            nome="Auditoria Interna"
        )
        self.tipo_constatacao = TipoConstatacao.objects.create(
            tenant=self.tenant,
            nome="Não Conformidade Menor",
            severidade=2
        )
        self.processo = Processo.objects.create(
            tenant=self.tenant,
            codigo="PROC001",
            nome="Processo Teste"
        )
        self.auditoria = Auditoria.objects.create(
            tenant=self.tenant,
            codigo="AUD-2024-0001",
            titulo="Auditoria de Teste",
            tipo=self.tipo_auditoria,
            objetivo="Objetivo",
            escopo="Escopo",
            data_planejada_inicio=timezone.now().date(),
            data_planejada_fim=timezone.now().date() + timedelta(days=7),
            auditor_lider=self.user,
            criado_por=self.user
        )
        self.constatacao = Constatacao.objects.create(
            tenant=self.tenant,
            auditoria=self.auditoria,
            numero="CONST-2024-0001",
            tipo=self.tipo_constatacao,
            processo=self.processo,
            titulo="Constatação Teste",
            descricao="Descrição",
            evidencia="Evidência",
            responsavel=self.user,
            prazo_resposta=timezone.now().date() + timedelta(days=30),
            criado_por=self.user
        )
        self.acao = AcaoCorretiva.objects.create(
            tenant=self.tenant,
            constatacao=self.constatacao,
            numero="AC-2024-0001",
            tipo="corretiva",
            descricao="Ação corretiva teste",
            objetivo="Corrigir o problema",
            responsavel=self.user,
            prazo_conclusao=timezone.now().date() + timedelta(days=15),
            criado_por=self.user
        )
    
    def test_acao_criacao(self):
        """Testar criação de ação corretiva"""
        self.assertEqual(self.acao.numero, "AC-2024-0001")
        self.assertEqual(self.acao.tipo, "corretiva")
        self.assertEqual(self.acao.status, "planejada")
    
    def test_acao_str(self):
        """Testar representação string da ação"""
        self.assertTrue(self.acao.numero in str(self.acao))
