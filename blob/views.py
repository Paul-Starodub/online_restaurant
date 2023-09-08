from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from blob.forms import PostCustomizeForm
from blob.models import Post, Commentary
from dishes.models import Dish


class PostListView(LoginRequiredMixin, generic.ListView):
    queryset = Post.objects.select_related("dish", "user").prefetch_related(
        "commentaries__user"
    )
    paginate_by = 2


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostCustomizeForm
    template_name = "blob/post_form.html"

    def __init__(self, **kwargs: dict) -> None:
        super().__init__(**kwargs)
        self.object = None

    def form_valid(self, form: PostCustomizeForm) -> HttpResponseRedirect:
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.dish = get_object_or_404(Dish, pk=self.kwargs["pk"])
        self.object.save()
        return redirect("posts:post-detail", pk=self.object.pk)


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Post.objects.select_related(
        "dish__dish_type", "user"
    ).prefetch_related("commentaries__user")


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ("description", "rating")


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("posts:post-list")


class CommentaryCreateView(LoginRequiredMixin, generic.CreateView):
    queryset = Commentary.objects.select_related("post__user")
    fields = ("content",)
    template_name = "blob/commentary_form.html"

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("posts:post-detail", args=[self.kwargs["pk"]])


class CommentaryDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Commentary.objects.select_related(
        "post__dish__dish_type", "user"
    )
    context_object_name = "comment"


class CommentaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Commentary
    success_url = reverse_lazy("posts:post-list")
