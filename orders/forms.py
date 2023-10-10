from django import forms
from phonenumber_field.formfields import PhoneNumberField

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(), required=True)
    last_name = forms.CharField(widget=forms.TextInput(), required=True)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "example@gmail.com"}),
        required=True,
    )
    phone = PhoneNumberField(
        region="UA",
        widget=forms.TextInput(attrs={"placeholder": "Enter phone number"}),
        required=True,
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ukraine, Lviv, Franko, 78",
            }
        ),
        required=True,
    )

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "email", "address", "phone")
