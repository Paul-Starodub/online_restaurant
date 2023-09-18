from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import (
    CustomerCreateView,
    CustomerProfileView,
    EmailVerificationView,
)

urlpatterns = [
    path("create/", CustomerCreateView.as_view(), name="user-create"),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "profile/<int:pk>", CustomerProfileView.as_view(), name="user-profile"
    ),
    path(
        "logout/", LogoutView.as_view(), name="logout"
    ),  # logout works without this url
    path(
        "verify/<str:email>/<uuid:code>/",
        EmailVerificationView.as_view(),
        name="email_verification",
    ),
]

app_name = "users"
