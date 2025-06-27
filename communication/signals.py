from django.dispatch import receiver
from communication.models import Message
from django.db.models.signals import post_save
from communication.tasks import send_email_to_tenant


@receiver(post_save, sender=Message)
def post_save_message(sender, instance, created, **kwargs):
    try:
        if created:
            send_email_to_tenant.delay()
    except Exception as e:
        raise str(e)
