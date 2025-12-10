from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List

from django.core.files.base import ContentFile
from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F, Sum
from django.utils import timezone

from .models import (
    Auditoria,
    AuditoriaStatus,
    Constatacao,
    ConstatacaoTipo,
    Criticidade,
    RelatorioAuditoria,
    SeguimentoStatus,
    SeguimentoAuditoria,
)


def safe_div(num: float, denom: float) -> float:
    if not denom:
        return 0.0
    return round(num / denom, 2)


def transition_auditoria(auditoria: Auditoria, novo_status: str) -> Auditoria:
    if novo_status == AuditoriaStatus.EM_EXECUCAO and not auditoria.data_real_inicio:
        auditoria.data_real_inicio = timezone.now().date()
    if novo_status in (AuditoriaStatus.CONCLUIDA, AuditoriaStatus.CANCELADA) and not auditoria.data_real_fim:
        auditoria.data_real_fim = timezone.now().date()
    auditoria.status = novo_status
    auditoria.save(update_fields=['status', 'data_real_inicio', 'data_real_fim', 'atualizado_em'])
    return auditoria


def _tempo_medio_execucao():
    auditorias = Auditoria.objects.exclude(data_real_inicio__isnull=True).exclude(data_real_fim__isnull=True)
    if not auditorias.exists():
        return 0.0
    delta = auditorias.aggregate(
        media=Avg(
            ExpressionWrapper(
                F('data_real_fim') - F('data_real_inicio'),
                output_field=DurationField(),
            )
        )
    )['media']
    if delta is None:
        return 0.0
    return round(delta.total_seconds() / 86400, 2)


def calculate_kpis() -> Dict:
    auditorias = Auditoria.objects.all()
    total_planeado = auditorias.count()
    realizadas = auditorias.filter(status=AuditoriaStatus.CONCLUIDA).count()
    percentual_execucao = safe_div(realizadas * 100, total_planeado)

    constatacoes = Constatacao.objects.all()
    constatacoes_por_auditoria = safe_div(constatacoes.count(), total_planeado)

    processos_counter = list(
        Constatacao.objects.values('processo__id', 'processo__nome')
        .exclude(processo__isnull=True)
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    departamentos_counter = list(
        Constatacao.objects.values('departamento__id', 'departamento__nome')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    seguimentos = SeguimentoAuditoria.objects.all()
    total_acoes = seguimentos.aggregate(total=Sum('acoes_planejadas'))['total'] or 0
    total_implementadas = seguimentos.aggregate(total=Sum('acoes_implementadas'))['total'] or 0
    taxa_eficacia = safe_div(total_implementadas * 100, total_acoes or 1)
    total_seguimentos = seguimentos.count() or 1

    kpis = {
        'auditorias_planeadas': total_planeado,
        'auditorias_realizadas': realizadas,
        'percentual_execucao': percentual_execucao,
        'tempo_medio_execucao': _tempo_medio_execucao(),
        'constatacoes_por_auditoria': constatacoes_por_auditoria,
        'taxa_nc_por_processo': [
            {'processo_id': p['processo__id'], 'processo_nome': p['processo__nome'], 'total': p['total']}
            for p in processos_counter
        ],
        'acoes_corretivas_prazo': safe_div(
            seguimentos.filter(status=SeguimentoStatus.CONCLUIDO).count() * 100,
            total_seguimentos,
        ),
        'tempo_fecho_nc': 0,
        'evolucao_conformidade': [],
        'top_processos_nc': processos_counter[:5],
        'top_departamentos_om': departamentos_counter[:5],
        'taxa_eficacia': taxa_eficacia,
    }

    return kpis


def build_dashboard_payload() -> Dict:
    auditorias_por_status = {
        row['status']: row['total']
        for row in Auditoria.objects.values('status').annotate(total=Count('id'))
    }

    timeline = (
        Auditoria.objects.extra({'mes': "strftime('%m', data_prevista_inicio)", 'ano': "strftime('%Y', data_prevista_inicio)"})
        .values('ano', 'mes')
        .annotate(total=Count('id'))
        .order_by('ano', 'mes')
    )

    mapa_calor = (
        Constatacao.objects.values('departamento__nome', 'tipo')
        .annotate(total=Count('id'))
        .order_by('departamento__nome')
    )

    programa = {
        'por_tipo': {
            row['tipo']: row['total']
            for row in Auditoria.objects.values('tipo').annotate(total=Count('id'))
        },
        'por_trimestre': _auditorias_por_trimestre(),
    }

    constatacoes_payload = {
        'por_criticidade': {
            row['criticidade']: row['total']
            for row in Constatacao.objects.values('criticidade').annotate(total=Count('id'))
        },
        'por_tipo': {
            row['tipo']: row['total']
            for row in Constatacao.objects.values('tipo').annotate(total=Count('id'))
        },
    }

    seguimento_payload = {
        'por_status': {
            row['status']: row['total']
            for row in SeguimentoAuditoria.objects.values('status').annotate(total=Count('id'))
        },
        'acoes_atrasadas': SeguimentoAuditoria.objects.aggregate(total=Sum('acoes_atrasadas'))['total'] or 0,
    }

    return {
        'kpis': calculate_kpis(),
        'auditorias_por_status': auditorias_por_status,
        'timeline': list(timeline),
        'mapa_calor': list(mapa_calor),
        'programa': programa,
        'constatacoes': constatacoes_payload,
        'seguimento': seguimento_payload,
    }


def _auditorias_por_trimestre() -> Dict[str, int]:
    resultado = {'T1': 0, 'T2': 0, 'T3': 0, 'T4': 0}
    for auditoria in Auditoria.objects.all():
        mes = auditoria.data_prevista_inicio.month
        if mes <= 3:
            resultado['T1'] += 1
        elif mes <= 6:
            resultado['T2'] += 1
        elif mes <= 9:
            resultado['T3'] += 1
        else:
            resultado['T4'] += 1
    return resultado


def generate_relatorio_pdf(relatorio: RelatorioAuditoria) -> str:
    conteudo = f"Relatório da Auditoria {relatorio.auditoria.numero_sequencial}\n\n{relatorio.resumo_executivo}"
    filename = f"relatorio_{relatorio.auditoria.numero_sequencial}.txt"
    relatorio.arquivo_pdf.save(filename, ContentFile(conteudo.encode('utf-8')), save=True)
    return relatorio.arquivo_pdf.url
