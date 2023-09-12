from django.urls import path
from django.contrib.auth.views import LoginView

from users.views import CustomerCreateView, ProfileView

urlpatterns = [
    path("create/", CustomerCreateView.as_view(), name="user-create"),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path("profile/", ProfileView.as_view(), name="user-profile"),
]

app_name = "users"
