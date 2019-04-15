import uuid

from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    user_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=128, default='')
    last_name = models.CharField(max_length=128, default='')
    username = models.CharField(max_length=128, default='', unique=True)
    email = models.CharField(max_length=128, default='')
    password = models.CharField(max_length=128, default='')

    @classmethod
    def create_user(cls, **kwargs):
        user = User(**kwargs)
        user.set_password(user.password)
        user.save()
        return user

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
