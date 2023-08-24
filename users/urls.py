from django.urls import path

from users.views import CustomerCreateView

urlpatterns = [
    path("create/", CustomerCreateView.as_view(), name="user-create"),
]

app_name = "users"
