import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)

    @classmethod
    def create_user(cls, **kwargs):
        user = User(**kwargs)
        user.set_password(user.password)
        user.save()
        return user
