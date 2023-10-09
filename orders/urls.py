from django.urls import path

from orders.views import (
    OrderCreateView,
    SuccessTemplateView,
    CanceledTemplateView,
    OrderListView,
)

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("", OrderListView.as_view(), name="order-list"),
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
