from django.apps import AppConfig


class JoinuptestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "JoinUPTest"

    def ready(self):
        from . import receivers
        super().ready()
