from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

@shared_task
def add(x, y):
    return x+y

@shared_task
def task_mail_register(pk=None):
    user = User.objects.get(pk=pk)
    msg = EmailMessage(
        subject='Register',
        body=' ',
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    msg.template_id = '5c97418c-60d4-4694-be9e-2eb5e5390ce6'
    msg.substitutions = {
        ':username': user.username
    }
    msg.send()
    return user.pk
