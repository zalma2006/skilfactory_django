from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from django.template.loader import render_to_string
import os


@receiver(post_save, sender=Appointment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    html_content = render_to_string(
        'appointment_created.html',
        {
            'appointment': instance,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'{instance.client_name} {instance.date.strftime("%d.%m.%Y")}',
        body=instance.message,
        from_email=str(os.getenv('FROM_EMAIL')),
        to=[str(instance.email)]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
