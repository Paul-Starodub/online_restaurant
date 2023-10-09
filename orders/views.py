from http import HTTPStatus

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from dishes.models import Basket
from orders.forms import OrderForm
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "orders/success.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        session_id = request.GET.get("session_id")

        if session_id:
            # Retrieve information from Stripe session metadata
            session = stripe.checkout.Session.retrieve(session_id)
            user_id = session.metadata.get("user_id")

            if user_id:
                try:
                    user = get_user_model().objects.get(id=user_id)
                    user.backend = (
                        "allauth.account.auth_backends.AuthenticationBackend"
                    )
                    login(request, user)
                except get_user_model().DoesNotExist:
                    return HttpResponseBadRequest(
                        "User does not exist", status=HTTPStatus.BAD_REQUEST
                    )
        return super().get(request, *args, **kwargs)


class CanceledTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "orders/canceled.html"


class OrderListView(generic.ListView):
    template_name = "orders/orders.html"
    ordering = ("-created",)

    def get_queryset(self) -> QuerySet:
        queryset = Order.objects.select_related("initiator")
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "orders/order.html"
    model = Order


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
            metadata={
                "order_id": self.object.id,
                "user_id": self.request.user.id,  # save user
            },
            mode="payment",
            success_url="{}{}".format(
                settings.DOMAIN_NAME, reverse("orders:order-success")
            )
            + "?session_id={CHECKOUT_SESSION_ID}",
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
        print(e)
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        print(e)
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session) -> None:
    order_id = int(session.metadata.order_id)
    order = get_object_or_404(Order, id=order_id)
    order.update_after_payment()
