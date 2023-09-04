from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _


def validate_ukrainian_phone_number(value: str) -> None:
    pattern = r"^\+380\d{9}$"

    import re

    if not re.match(pattern, value):
        raise ValidationError(
            "Incorrect phone number. Example: +380971234567."
        )


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    phone = PhoneNumberField(
        unique=True,
        region="UA",
        blank=True,
        validators=[validate_ukrainian_phone_number],
    )

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return self.username
