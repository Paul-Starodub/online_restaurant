from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User
from phonenumber_field.formfields import PhoneNumberField


class CustomerCreationForm(UserCreationForm):
    phone = PhoneNumberField(region="UA")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "phone", "image")


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
