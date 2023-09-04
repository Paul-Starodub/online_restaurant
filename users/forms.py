from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from users.models import User
from phonenumber_field.formfields import PhoneNumberField


class CustomerCreationForm(UserCreationForm):
    phone = PhoneNumberField(
        region="UA",
        widget=PhoneNumberPrefixWidget(
            country_choices=[
                ("UA", "Ukraine"),
            ],
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "phone")
