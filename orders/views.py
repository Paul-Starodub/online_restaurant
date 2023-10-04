from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect

from orders.forms import OrderForm


class OrderCreateView(CreateView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:order-create")

    def get_initial(self) -> dict:
        initial = super().get_initial()
        user = self.request.user

        if user.is_authenticated:
            initial["first_name"] = user.first_name
            initial["last_name"] = user.last_name
            initial["email"] = user.email
            initial["phone"] = user.phone

        return initial

    def form_valid(self, form: OrderForm) -> HttpResponseRedirect:
        form.instance.initiator = self.request.user
        return super().form_valid(form)
