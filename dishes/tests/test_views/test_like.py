from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Dish


class UpdateLikeViewTestCase(TestCase):
    fixtures = ["restaurant_data.json"]

    def test_update_like_view(self) -> None:
        self.user = get_user_model().objects.last()
        self.dish = Dish.objects.first()
        self.client.force_login(self.user)
        url = reverse("cuisine:update_like_dish", kwargs={"pk": self.dish.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user in self.dish.likes.all())

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user in self.dish.likes.all())
