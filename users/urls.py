from django.urls import path
from django.contrib.auth.views import LoginView

from users.views import CustomerCreateView

urlpatterns = [
    path("create/", CustomerCreateView.as_view(), name="user-create"),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
]

app_name = "users"
