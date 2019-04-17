import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template import loader
from django_q.tasks import async_task

from .user import User

NEW_SUBSCRIBER_NOTICE_TITLE_PATH = 'new_subscriber_notice_title.txt'
NEW_SUBSCRIBER_NOTICE = 'new_subscriber_notice.txt'


class Subscription(models.Model):
    subs_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_subs')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_subs')

    class Meta:
        unique_together = ('owner', 'target',)

    @classmethod
    def get_outgoing(cls, owner_id):
        return cls.objects.filter(owner__user_id=owner_id).all()

    @classmethod
    def get_incoming(cls, target_id):
        return cls.objects.filter(target__user_id=target_id).all()

    @classmethod
    def get(cls, owner_id, target_id):
        return cls.objects.get(owner__user_id=owner_id, target__user_id=target_id)


def render_template(template_path: str, context: dict) -> str:
    template = loader.get_template(template_path)
    return template.render(context)


def send_email(title: str, message: str, to: str) -> None:
    async_task(
        'django.core.mail.send_mail',
        title,
        message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to]
    )


@receiver(pre_save, sender=Subscription)
def subscription_added(sender, instance, **kwargs):
    context = dict(subscriber=instance.owner)
    notice_title = render_template(NEW_SUBSCRIBER_NOTICE_TITLE_PATH, context)
    notice = render_template(NEW_SUBSCRIBER_NOTICE, context)
    send_email(notice_title, notice, instance.target.email)
