from django.urls import path

from orders.views import (
    OrderCreateView,
    SuccessTemplateView,
    CanceledTemplateView,
)

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path(
        "order-success/", SuccessTemplateView.as_view(), name="order-success"
    ),
    path(
        "order-canceled/",
        CanceledTemplateView.as_view(),
        name="order-canceled",
    ),
]

app_name = "orders"
