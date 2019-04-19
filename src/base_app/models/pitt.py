import uuid

from django.db import models

from .user import User


def user_directory_path(instance, filename):
    return 'user_{}/{}'.format(instance.user.id, filename)


class Pitt(models.Model):
    pitt_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    audio = models.FileField(upload_to=user_directory_path)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.objects.filter(user__user_id=user_id).all()
