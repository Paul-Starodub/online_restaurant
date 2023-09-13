from django import forms

from blog.models import Post


class PostCustomizeForm(forms.ModelForm):
    RATING_CHOICES = (
        (1, "very bad"),
        (2, "bad"),
        (3, "maybe"),
        (4, "good"),
        (5, "excellent"),
    )
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label="Rating of this dish",
    )

    class Meta:
        model = Post
        fields = ("description", "rating")
