from django.dispatch import receiver
from django.db.models.signals import post_save
from maintenance.models import MaintenanceRequest
from maintenance.tasks import maintenance_request_email


@receiver(post_save, sender=MaintenanceRequest)
def post_save_maintenance_request(sender, instance, created, **kwargs):
    try:
        if created:
            maintenance_request_email.delay()
    except Exception as e:
        raise str(e)
