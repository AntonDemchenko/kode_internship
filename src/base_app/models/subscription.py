import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_q.tasks import async_task

from .user import User


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


@receiver(pre_save, sender=Subscription)
def subscription_added(sender, instance, **kwargs):
    async_task(
        'django.core.mail.send_mail',
        'Subscription',
        'User {} is subscribed on you'.format(instance.owner.username),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[instance.target.email]
    )
