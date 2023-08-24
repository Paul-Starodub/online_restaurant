from django.urls import path

from dishes.views import DishListView, DishTypeListView

urlpatterns = [
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("types/", DishTypeListView.as_view(), name="dish_type-list"),
]

app_name = "dishes"
