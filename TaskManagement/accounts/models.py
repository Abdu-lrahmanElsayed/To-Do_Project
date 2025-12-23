from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username