import uuid
from time import sleep

from celery import shared_task
from django.db.models.signals import post_save

from JoinUPTest.custom_decorators import receiver_with_multiple_senders
from JoinUPTest.models import User, ActivationCode, ActivationCodeType


@receiver_with_multiple_senders(
    [post_save],
    senders=[
        User,
        ActivationCode
    ],
)
def on_create_signal(sender, instance=None, created=False, **kwargs):
    if created:
        if sender is User:
            create_activation_codes(instance)
        if sender is ActivationCode:
            send_activation_codes.delay(instance.user_id, instance.type, instance.url)


def create_activation_codes(instance):
    ActivationCode(user=instance, type=ActivationCodeType.SMS, code=uuid.uuid4()).save()
    ActivationCode(user=instance, type=ActivationCodeType.EMAIL, code=uuid.uuid4()).save()


@shared_task
def send_activation_codes(user_id, code_type, url):
    sleep(5)
    if code_type == ActivationCodeType.SMS:
        User.objects.get(id=user_id).sms_user(url)
    if code_type == ActivationCodeType.EMAIL:
        User.objects.get(id=user_id).email_user(url)
