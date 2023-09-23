import os

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

INDEX_URL = reverse("cuisine:index")


class PublicIndexTestCase(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(INDEX_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTestCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="Test email",
            password="Test password",
            username="Test username",
        )
        self.client.force_login(self.user)

    def test_retrieve_index(self) -> None:
        response1 = self.client.get(INDEX_URL)
        response2 = self.client.get(INDEX_URL)

        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response2, "dishes/index.html")
        self.assertEqual(response2.context["num_visits"], 2)
        self.assertEqual(response1.context["count_dishes"], 0)
        self.assertEqual(response1.context["count_dish_types"], 0)
        self.assertEqual(response1.context["contact"], os.getenv("CONTACT"))
