from django.contrib.auth.forms import UserCreationForm

from users.models import User
from phonenumber_field.formfields import PhoneNumberField


class CustomerCreationForm(UserCreationForm):
    phone = PhoneNumberField(region="UA")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "phone")
