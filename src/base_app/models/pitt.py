import uuid

from django.db import models

from .user import User


class Pitt(models.Model):
    pitt_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    audio = models.TextField()
    text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.objects.filter(user__user_id=user_id).all()

    @classmethod
    def get_by_id(cls, pitt_id):
        return cls.objects.get(pitt_id=pitt_id)
