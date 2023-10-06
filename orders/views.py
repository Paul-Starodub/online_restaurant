import stripe

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from http import HTTPStatus

from orders.forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TemplateView):
    template_name = "orders/success.html"


class CanceledTemplateView(TemplateView):
    template_name = "orders/canceled.html"


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:order-create")

    def post(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponseRedirect:
        super().post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1NyF8MEh4Z78jXQXCoQOq8WX",
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="{}{}".format(
                settings.DOMAIN_NAME, reverse("orders:order-success")
            ),
            cancel_url="{}{}".format(
                settings.DOMAIN_NAME, reverse("orders:order-canceled")
            ),
        )
        return HttpResponseRedirect(
            checkout_session.url, status=HTTPStatus.SEE_OTHER
        )

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


@csrf_exempt
def stripe_webhook_view(request: HttpRequest) -> HttpResponse:
    payload = request.body

    # For now, you only need to print out the webhook payload so you can see
    # the structure.
    print(payload)

    return HttpResponse(status=200)
