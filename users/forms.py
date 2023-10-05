from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from phonenumber_field.formfields import PhoneNumberField

from users.models import User
from users.tasks import send_email_verification


def validate_unique_phone_or_empty(value: str) -> None:
    if value:
        if (
            get_user_model()
            .objects.filter(phone=value)
            .exclude(phone="")
            .exists()
        ):
            raise ValidationError("The number must be unique.")


class CustomerCreationForm(UserCreationForm):
    phone = PhoneNumberField(
        region="UA", validators=[validate_unique_phone_or_empty]
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "phone", "image")

    def save(self, commit=True) -> User:
        user = super().save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    phone = PhoneNumberField(
        region="UA",
        required=False,
    )

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

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone")
        if phone:
            users_with_same_phone = (
                get_user_model()
                .objects.exclude(pk=self.instance.pk)
                .filter(phone=phone)
            )
            if users_with_same_phone.exists():
                raise ValidationError(
                    "This phone number is already registered."
                )
        return phone
