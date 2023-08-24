from django.conf import settings
from django.db import models
from django.urls import reverse


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

    class Meta:
        ordering = ["-created_time"]

    def __str__(self) -> str:
        return self.description[:25]

    def get_absolute_url(self) -> str:
        return reverse("blog:post-detail", kwargs={"pk": self.pk})


class Commentary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
