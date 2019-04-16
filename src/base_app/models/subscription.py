import uuid

from django.db import models

from .user import User


class Subscription(models.Model):
    subs_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_subs')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_subs')

    @classmethod
    def get_outgoing_subs(cls, user_id):
        return cls.objects.filter(owner__user_id=user_id).all()

    @classmethod
    def get_incoming_subs(cls, user_id):
        return cls.objects.filter(target__user_id=user_id).all()
