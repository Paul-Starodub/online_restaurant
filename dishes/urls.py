from django.urls import path

from blob.views import PostCreateView
from dishes.views import (
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    DishTypeListView,
    DishTypeDetailView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    UpdateLikeView,
)

urlpatterns = [
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path(
        "dishes/<int:pk>/like/",
        UpdateLikeView.as_view(),
        name="update_like_dish",
    ),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path(
        "dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"
    ),
    path(
        "dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"
    ),
    path(
        "dishes/<int:pk>/create_post/",
        PostCreateView.as_view(),
        name="post-create",
    ),
    path("types/", DishTypeListView.as_view(), name="dish_type-list"),
    path(
        "types/<int:pk>/",
        DishTypeDetailView.as_view(),
        name="dish_type-detail",
    ),
    path(
        "types/create/", DishTypeCreateView.as_view(), name="dish_type-create"
    ),
    path(
        "types/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dish_type-update",
    ),
    path(
        "types/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dish_type-delete",
    ),
]

app_name = "cuisine"
