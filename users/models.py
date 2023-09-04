from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    phone = PhoneNumberField(unique=True, region="UA", blank=True)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return self.username
