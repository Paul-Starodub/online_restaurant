from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from blob.forms import PostCustomizeForm
from blob.models import Post


class PostListView(LoginRequiredMixin, generic.ListView):
    template_name = "posts/post_list.html"
    queryset = Post.objects.select_related("user", "dish")
    paginate_by = 2


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostCustomizeForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("posts:post-list")

    def form_valid(self, form: PostCustomizeForm) -> HttpResponseRedirect:
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
