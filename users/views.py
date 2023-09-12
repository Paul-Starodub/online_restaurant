from django.views import generic
from django.views.generic.edit import FormView


from users.forms import CustomerCreationForm, UserProfileForm
from users.models import User
from django.urls import reverse_lazy


class CustomerCreateView(generic.CreateView):
    model = User
    form_class = CustomerCreationForm
    success_url = reverse_lazy("users:login")


# Example alternative solution(without handling errors)
# class ProfileView(generic.View):
#     template_name = "users/profile.html"
#
#     def get(self, request, *args, **kwargs):
#         form = UserProfileForm(instance=request.user)
#         context = {"form": form}
#         return render(request, self.template_name, context=context)
#
#     def post(self, request, *args, **kwargs):
#         form = UserProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("users:user-profile"))
#         context = {"form": form}
#         return render(request, self.template_name, context=context)


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
