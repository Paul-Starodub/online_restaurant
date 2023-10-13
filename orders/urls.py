from django.urls import path

from orders.views import (
    CanceledTemplateView,
    OrderCreateView,
    OrderDetailView,
    OrderListView,
    SuccessTemplateView,
)

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("", OrderListView.as_view(), name="order-list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
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
