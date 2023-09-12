from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import CustomerCreateView, ProfileView

urlpatterns = [
    path("create/", CustomerCreateView.as_view(), name="user-create"),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path("profile/", ProfileView.as_view(), name="user-profile"),
    path(
        "logout/", LogoutView.as_view(), name="logout"
    ),  # logout works without this url
]

app_name = "users"
