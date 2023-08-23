from django.urls import path

from dishes.views import DishListView

urlpatterns = [
    path("", DishListView.as_view(), name="dish-list"),
]

app_name = "dishes"
