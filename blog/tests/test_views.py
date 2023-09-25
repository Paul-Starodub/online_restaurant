from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from blog.models import Post, Commentary
from dishes.models import Dish


class PostCreateViewTestCase(TestCase):
    fixtures = ["restaurant_data.json"]

    def setUp(self) -> None:
        self.dish = Dish.objects.last()
        self.user = get_user_model().objects.last()
        self.client.force_login(self.user)

    def test_post_create_view(self) -> None:
        form_data = {
            "description": "Test Post",
            "rating": 3,
            "dish": self.dish.id,
        }

        url = reverse("cuisine:post-create", kwargs={"pk": self.dish.pk})
        response = self.client.post(url, data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 3)


class CommentaryCreateViewTestCase(TestCase):
    fixtures = ["restaurant_data.json"]

    def setUp(self) -> None:
        self.post = Post.objects.last()
        self.user = get_user_model().objects.last()
        self.client.force_login(self.user)

    def test_comment_create_view(self) -> None:
        form_data = {"content": "red"}

        url = reverse("posts:comment-create", kwargs={"pk": self.post.pk})
        response = self.client.post(url, data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Commentary.objects.count(), 2)
