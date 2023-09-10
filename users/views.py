from django.contrib.auth import login
from django.http import HttpResponseRedirect

from django.views import generic

from users.forms import CustomerCreationForm
from users.models import User
from django.urls import reverse_lazy


class CustomerCreateView(generic.CreateView):
    model = User
    form_class = CustomerCreationForm
    success_url = reverse_lazy("cuisine:dish-list")

    def form_valid(self, form: CustomerCreationForm) -> HttpResponseRedirect:
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
