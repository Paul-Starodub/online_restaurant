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
from dishes.models import Basket

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
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={"order_id": self.object.id},
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
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    # TODO: fill me in
    order_id = int(session.metadata.order_id)
    # print("Fulfilling order")
