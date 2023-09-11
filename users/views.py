from django.views import generic


from users.forms import CustomerCreationForm
from users.models import User
from django.urls import reverse_lazy


class CustomerCreateView(generic.CreateView):
    model = User
    form_class = CustomerCreationForm
    success_url = reverse_lazy("users:login")
