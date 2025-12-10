from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Constatacao, AcaoCorretiva, Auditoria


@receiver(post_save, sender=Constatacao)
def notificar_nova_constatacao(sender, instance, created, **kwargs):
    """
    Notificar responsável quando uma nova constatação é criada
    """
    if created:
        # Aqui você pode implementar notificação por email, SMS, etc.
        if hasattr(settings, 'EMAIL_NOTIFICATIONS') and settings.EMAIL_NOTIFICATIONS:
            if instance.responsavel.email:
                send_mail(
                    subject=f'Nova Constatação: {instance.numero}',
                    message=f'''
                    Você foi designado como responsável pela constatação {instance.numero}.
                    
                    Título: {instance.titulo}
                    Auditoria: {instance.auditoria}
                    Prazo: {instance.prazo_resposta}
                    
                    Por favor, acesse o sistema para mais detalhes.
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.responsavel.email],
                    fail_silently=True,
                )


@receiver(post_save, sender=AcaoCorretiva)
def notificar_nova_acao(sender, instance, created, **kwargs):
    """
    Notificar responsável quando uma nova ação corretiva é criada
    """
    if created:
        if hasattr(settings, 'EMAIL_NOTIFICATIONS') and settings.EMAIL_NOTIFICATIONS:
            if instance.responsavel.email:
                send_mail(
                    subject=f'Nova Ação Corretiva: {instance.numero}',
                    message=f'''
                    Você foi designado como responsável pela ação corretiva {instance.numero}.
                    
                    Constatação: {instance.constatacao}
                    Tipo: {instance.get_tipo_display()}
                    Prazo: {instance.prazo_conclusao}
                    
                    Por favor, acesse o sistema para mais detalhes.
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.responsavel.email],
                    fail_silently=True,
                )


@receiver(pre_save, sender=Auditoria)
def gerar_codigo_auditoria(sender, instance, **kwargs):
    """
    Gerar código automático para auditoria se não fornecido
    """
    if not instance.codigo and instance.tenant:
        # Gerar código no formato AUD-YYYY-NNNN
        from django.utils import timezone
        ano = timezone.now().year
        ultima = Auditoria.objects.filter(
            tenant=instance.tenant,
            codigo__startswith=f'AUD-{ano}'
        ).order_by('-codigo').first()
        
        if ultima:
            try:
                numero = int(ultima.codigo.split('-')[-1]) + 1
            except:
                numero = 1
        else:
            numero = 1
        
        instance.codigo = f'AUD-{ano}-{numero:04d}'


@receiver(pre_save, sender=Constatacao)
def gerar_numero_constatacao(sender, instance, **kwargs):
    """
    Gerar número automático para constatação se não fornecido
    """
    if not instance.numero and instance.tenant:
        # Gerar número no formato CONST-YYYY-NNNN
        from django.utils import timezone
        ano = timezone.now().year
        ultima = Constatacao.objects.filter(
            tenant=instance.tenant,
            numero__startswith=f'CONST-{ano}'
        ).order_by('-numero').first()
        
        if ultima:
            try:
                numero = int(ultima.numero.split('-')[-1]) + 1
            except:
                numero = 1
        else:
            numero = 1
        
        instance.numero = f'CONST-{ano}-{numero:04d}'


@receiver(pre_save, sender=AcaoCorretiva)
def gerar_numero_acao(sender, instance, **kwargs):
    """
    Gerar número automático para ação corretiva se não fornecido
    """
    if not instance.numero and instance.tenant:
        # Gerar número no formato AC-YYYY-NNNN
        from django.utils import timezone
        ano = timezone.now().year
        ultima = AcaoCorretiva.objects.filter(
            tenant=instance.tenant,
            numero__startswith=f'AC-{ano}'
        ).order_by('-numero').first()
        
        if ultima:
            try:
                numero = int(ultima.numero.split('-')[-1]) + 1
            except:
                numero = 1
        else:
            numero = 1
        
        instance.numero = f'AC-{ano}-{numero:04d}'
