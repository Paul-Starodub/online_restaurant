from django.urls import path

from dishes.views import (
    DishListView,
    DishTypeListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    UpdateLikeView,
)

urlpatterns = [
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("types/", DishTypeListView.as_view(), name="dish_type-list"),
    path(
        "dishes/<int:pk>/like/",
        UpdateLikeView.as_view(),
        name="update_like_dish",
    ),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path(
        "dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"
    ),
]

app_name = "cuisine"
