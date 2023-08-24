from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return self.username
