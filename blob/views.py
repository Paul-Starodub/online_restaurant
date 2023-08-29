from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from blob.models import Post


class PostListView(LoginRequiredMixin, generic.ListView):
    template_name = "posts/post_list.html"
    queryset = Post.objects.select_related("user")
    paginate_by = 2
