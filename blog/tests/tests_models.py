from django.test import TestCase
from django.urls import reverse

from blog.models import Commentary, Post


class PostTests(TestCase):
    fixtures = ["restaurant_data.json"]

    def setUp(self) -> None:
        self.post = Post.objects.last()
        self.commentary = Commentary.objects.last()

    def test_post_and_commentary_str(self) -> None:
        self.assertEqual(str(self.post), self.post.description[:7])
        self.assertEqual(
            str(self.commentary), f"posted by {self.commentary.user}"
        )

    def test_get_absolute_url(self) -> None:
        url = self.post.get_absolute_url()
        expected_url = reverse(
            "posts:post-detail", kwargs={"pk": self.post.pk}
        )

        self.assertEqual(url, expected_url)
