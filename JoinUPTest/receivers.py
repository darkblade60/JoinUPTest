import uuid

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
            ActivationCode(user=instance, type=ActivationCodeType.SMS, code=uuid.uuid4()).save()
            ActivationCode(user=instance, type=ActivationCodeType.EMAIL, code=uuid.uuid4()).save()
        if sender is ActivationCode:
            if instance.type == ActivationCodeType.SMS:
                instance.user.sms_user(instance.url)
            if instance.type == ActivationCodeType.EMAIL:
                instance.user.email_user(instance.url)


