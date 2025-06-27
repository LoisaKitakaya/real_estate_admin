import logging
from celery import shared_task
from django.conf import settings
from communication.models import Message
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@shared_task
def send_email_to_tenant():
    message = Message.objects.filter(is_delivered=False).first()

    if not message:
        logger.info("No undelivered messages found")

        return

    context = {
        "receiver": message.recipient.user.first_name,
        "message": message.body,
        "sender": f"{message.sender.first_name} {message.sender.last_name} - {message.sender.username}",
        "company_name": settings.ORGANIZATION_NAME,
    }

    subject = message.subject

    sender = message.sender.email

    receiver = message.recipient.user.email

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
            [receiver],
        )

        msg.attach_alternative(html_content, "text/html")

        msg.send()

    except Exception as e:
        logger.error(f"Error sending email: {e}", exc_info=True)
        
        raise
    else:
        message.is_delivered = True

        message.save()
