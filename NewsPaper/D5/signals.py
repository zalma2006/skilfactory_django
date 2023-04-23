from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from django.conf import settings
from D5.models import PostCategory
from .tasks import send_notifications


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category_id.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications.apply_async(kwargs={'preview': instance.preview(),
                                               'pk': instance.pk,
                                               'title': instance.title,
                                               'subscribers': subscribers_emails}, expires=30)
