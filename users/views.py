from django.views import generic
from django.views.generic.edit import FormView


from users.forms import CustomerCreationForm, UserProfileForm
from users.models import User
from django.urls import reverse_lazy


class CustomerCreateView(generic.CreateView):
    model = User
    form_class = CustomerCreationForm
    success_url = reverse_lazy("users:login")


class ProfileView(FormView):
    template_name = "users/profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("users:user-profile")

    def form_valid(self, form: UserProfileForm) -> None:
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self) -> dict[str, dict]:
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs
