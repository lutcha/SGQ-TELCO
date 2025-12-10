from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Auditoria, Constatacao, ConstatacaoTipo


def _sync_auditoria_metrics(auditoria_id: int):
    try:
        auditoria = Auditoria.objects.get(id=auditoria_id)
    except Auditoria.DoesNotExist:
        return
    total = auditoria.constatacoes.count()
    ncs = auditoria.constatacoes.filter(tipo=ConstatacaoTipo.NAO_CONFORMIDADE).count()
    oportunidades = auditoria.constatacoes.filter(tipo=ConstatacaoTipo.OPORTUNIDADE_MELHORIA).count()

    Auditoria.objects.filter(id=auditoria_id).update(
        total_constatacoes=total,
        nao_conformidades_encontradas=ncs,
        oportunidades_melhoria=oportunidades,
    )


@receiver(post_save, sender=Constatacao)
def update_auditoria_metrics_on_save(sender, instance, **kwargs):
    _sync_auditoria_metrics(instance.auditoria_id)


@receiver(post_delete, sender=Constatacao)
def update_auditoria_metrics_on_delete(sender, instance, **kwargs):
    _sync_auditoria_metrics(instance.auditoria_id)
