import os
import uuid

from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _


def user_image_file_path(instance: User, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    from django.utils.text import slugify

    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/users/", filename)


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
    image = models.ImageField(
        upload_to=user_image_file_path, null=True, blank=True
    )

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return self.username
