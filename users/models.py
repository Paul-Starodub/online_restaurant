from __future__ import annotations
import os
import uuid
from django.core.mail import send_mail

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField


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
    is_verified_email = models.BooleanField(default=False)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return self.username


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="emails"
    )
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self) -> str:
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self) -> None:
        link = reverse(
            "users:email_verification",
            kwargs={"email": self.user.email, "code": self.code},
        )
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"account confirmation for {self.user}"
        message = (
            "To confirm your account for your {}, follow the link: {}".format(
                self.user.email, verification_link
            )
        )
        send_mail(
            subject=subject,
            message=message,
            from_email="from@example.com",
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self) -> bool:
        return True if now() >= self.expiration else False
