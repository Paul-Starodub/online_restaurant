from django.urls import path

from dishes.views import DishListView, DishTypeListView, DishDetailView

urlpatterns = [
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("types/", DishTypeListView.as_view(), name="dish_type-list"),
]

app_name = "cuisine"
