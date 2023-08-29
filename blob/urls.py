from django.urls import path

from blob.views import PostListView, PostCreateView

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("create/", PostCreateView.as_view(), name="post-create"),
]

app_name = "posts"
