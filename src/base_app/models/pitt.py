import uuid
from django.db import models

from base_app.models import User


class Pitt(models.Model):
    pitt_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    audio = models.BinaryField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
