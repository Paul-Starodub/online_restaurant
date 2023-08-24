from django.contrib.auth.forms import UserCreationForm

from users.models import User


class CustomerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
