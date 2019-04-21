import uuid

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_q.tasks import async_task

from base_app.utils.email import render_template, send_email
from .user import User

NEW_PITT_NOTICE_PATH = 'new_pitt_notice.txt'
NEW_PITT_NOTICE_TITLE_PATH = 'new_pitt_notice_title.txt'


class Pitt(models.Model):
    pitt_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    audio = models.TextField()
    text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pitts')

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.objects.filter(user__user_id=user_id).all()

    @classmethod
    def get_by_id(cls, pitt_id):
        return cls.objects.get(pitt_id=pitt_id)


def send_out_notices(pitt):
    context = dict(pitt=pitt)
    notice_title = render_template(NEW_PITT_NOTICE_TITLE_PATH, context)
    notice = render_template(NEW_PITT_NOTICE_PATH, context)
    for s in pitt.user.incoming_subs.all():
        send_email(notice_title, notice, to=s.owner.email)


@receiver(pre_save, sender=Pitt)
def pitt_added(sender, instance, **kwargs):
    async_task(
        send_out_notices,
        instance
    )
