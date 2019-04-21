from django.conf import settings
from django.template import loader
from django_q.tasks import async_task


def render_template(template_path: str, context: dict) -> str:
    template = loader.get_template(template_path)
    return template.render(context)


def send_email(title: str, message: str, to: str) -> None:
    async_task(
        'django.core.mail.send_mail',
        title,
        message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to]
    )
