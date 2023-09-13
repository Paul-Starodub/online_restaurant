from django.urls import path

from blog.views import (
    PostListView,
    PostUpdateView,
    PostDetailView,
    PostDeleteView,
    CommentaryCreateView,
    CommentaryDetailView,
    CommentaryDeleteView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path(
        "<int:pk>/commentaries/create/",
        CommentaryCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "commentaries/<int:pk>/",
        CommentaryDetailView.as_view(),
        name="commentary-detail",
    ),
    path(
        "commentaries/<int:pk>/delete/",
        CommentaryDeleteView.as_view(),
        name="commentary-delete",
    ),
]

app_name = "posts"
