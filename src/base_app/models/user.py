import uuid

from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=128, default='')
    last_name = models.CharField(max_length=128, default='')
    username = models.CharField(max_length=128, default='', unique=True)
    email = models.CharField(max_length=128, default='')
    password = models.CharField(max_length=128, default='')
