from django.apps import AppConfig


class SendMailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "send_mail"

    def ready(self):
        import send_mail.signals

        # from .tasks import send_mails
        from .scheduler import appointment_scheduler
        print('start')

        # appointment_scheduler.add_job(
        #     id='send_mail',
        #     func=send_mails,
        #     trigger='interval',
        #     seconds=10
        # )
        #
        # appointment_scheduler.start()

