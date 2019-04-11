import uuid
from django.db import models

from base_app.models import User


class Subscription(models.Model):
    subs_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target")
