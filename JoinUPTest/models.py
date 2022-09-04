from django.contrib.auth.models import User as BaseUser
from django.db import models
from twilio.rest import Client

from djangoProject import settings
from django_middleware_global_request import get_request


class ActivationCodeType:
    SMS = "SMS"
    EMAIL = "e-mail"

    TYPES = (
        (SMS, "SMS"),
        (EMAIL, "e-mail"),
    )


class User(BaseUser):
    phone_number = models.CharField(max_length=20, )
    hobbies_description = models.TextField()
    email_validated = models.BooleanField(default=False)
    phone_validated = models.BooleanField(default=False)

    def sms_user(self, url_activation):
        if settings.ACTIVATION_PROCESS:
            print("Sending sms....")
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=f"JoinUP verifica tu número : {url_activation}",
                    from_=settings.TWILIO_NUMBER,
                    to=self.phone_number
                 )
            except Exception as e:
                print("Número de telefono inválido")

    def email_user(self, url_activation):
        if settings.ACTIVATION_PROCESS:
            print("Sending email....")
            subject = "Bienvenido a JoinUP"
            message = "Tu usuario se ha creado correctamente, verifica tu correo : " + url_activation
            super().email_user(subject, message)

    def activate_phone(self):
        self.phone_validated = True
        self.save()

    def activate_email(self):
        self.email_validated = True
        self.save()

    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save(*args, **kwargs)


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,
                             blank=False, )
    type = models.CharField(
        max_length=20,
        choices=ActivationCodeType.TYPES,
        blank=False,
        null=False,
    )
    code = models.CharField(max_length=20, blank=False, default=False)

    @property
    def url(self):
        try:
            return f"http://{get_request().headers['Host']}/api/v1/activation/{self.code}"
        except Exception:
            return ""
