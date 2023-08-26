from django import forms

from dishes.models import Dish, DishType


class NameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class DishCustomizeForm(forms.ModelForm):
    dish_type = forms.ModelChoiceField(
        queryset=DishType.objects.all(), widget=forms.RadioSelect
    )

    class Meta:
        model = Dish
        fields = ("name", "description", "price", "image", "dish_type")
