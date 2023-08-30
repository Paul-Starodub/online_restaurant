from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from dishes.models import Dish


class Post(models.Model):
    RATING_CHOICES = (
        (1, "very bad"),
        (2, "bad"),
        (3, "maybe"),
        (4, "good"),
        (5, "excellent"),
    )
    description = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name="posts"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
    )

    class Meta:
        ordering = ["dish__name"]

    def __str__(self) -> str:
        return self.description[:7]

    def get_absolute_url(self) -> str:
        return reverse("blog:post-detail", kwargs={"pk": self.pk})


class Commentary(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="commentaries",
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="commentaries"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name="comment on post")

    class Meta:
        verbose_name_plural = "commentaries"
        ordering = ["-created_time"]

    def __str__(self) -> str:
        return f"posted by {self.user}"
