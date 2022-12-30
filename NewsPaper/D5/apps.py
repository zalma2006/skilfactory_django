from django.apps import AppConfig


class D5Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "D5"

    def ready(self):
        import D5.signals
