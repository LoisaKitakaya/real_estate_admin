import logging
from users.models import User
from celery import shared_task
from django.conf import settings
from django.utils.html import strip_tags
from maintenance.models import MaintenanceRequest
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@shared_task
def maintenance_request_email():
    maintenance_request = MaintenanceRequest.objects.filter(is_delivered=False).first()

    if not maintenance_request:
        logger.info("No undelivered maintenance requests found")

        return

    context = {
        "receiver": "Admin",
        "message": maintenance_request.description,
        "sender": f"{maintenance_request.tenant.user.first_name} {maintenance_request.tenant.user.last_name} - {maintenance_request.tenant.user.username}",
        "company_name": settings.ORGANIZATION_NAME,
    }

    subject = f"Maintenance Request For {str(maintenance_request.property)}"

    sender = maintenance_request.tenant.user.email

    admin_users = User.objects.filter(is_staff=True)

    try:
        html_content = render_to_string(
            "emails/message.html",
            context=context,
        )

        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            sender,
            [user.email for user in admin_users],
        )

        msg.attach_alternative(html_content, "text/html")

        msg.send()

    except Exception as e:
        logger.error(f"Error sending email: {e}", exc_info=True)

        raise
    else:
        maintenance_request.is_delivered = True

        maintenance_request.save()
