from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from mmorgnews.tasks import send_notifications


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


