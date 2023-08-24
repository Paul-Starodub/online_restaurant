from django.urls import reverse_lazy
from django.views import generic

from users.forms import CustomerCreationForm
from users.models import User


class CustomerCreateView(generic.CreateView):
    """Class for creating a new customer"""

    model = User
    form_class = CustomerCreationForm
    success_url = reverse_lazy("cuisine:dish-list")
