from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from users.forms import CustomerCreationForm, UserProfileForm
from users.models import EmailVerification, User


class CustomerCreateView(SuccessMessageMixin, generic.CreateView):
    model = User
    form_class = CustomerCreationForm
    success_url = reverse_lazy("users:login")
    success_message = "Congratulations! You have successfully registered"


class CustomerProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"

    def get_success_url(self) -> str:
        return reverse_lazy("users:user-profile", args=(self.object.id,))


class EmailVerificationView(generic.TemplateView):
    template_name = "users/email_verification.html"

    def get(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponseRedirect:
        code = kwargs["code"]
        user = get_object_or_404(User, email=kwargs["email"])
        email_verifications = EmailVerification.objects.filter(
            user=user, code=code
        )
        if (
            email_verifications.exists()
            and not email_verifications.first().is_expired()
        ):
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("cuisine:index"))
