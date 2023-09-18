import uuid
from datetime import timedelta

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.timezone import now
from phonenumber_field.formfields import PhoneNumberField

from users.models import EmailVerification, User


class CustomerCreationForm(UserCreationForm):
    phone = PhoneNumberField(region="UA")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "phone", "image")

    def save(self, commit=True) -> User:
        user = super().save(commit=True)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(
            code=uuid.uuid4(), user=user, expiration=expiration
        )
        record.send_verification_email()
        return user


class UserProfileForm(UserChangeForm):
    phone = PhoneNumberField(region="UA")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "image",
        )
