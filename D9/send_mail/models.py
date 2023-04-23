from django.db import models
from datetime import datetime as DT


class Appointment(models.Model):
    date = models.DateField(
        default=DT.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    email = models.EmailField(null=False, unique=False)
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}:{self.message}'

