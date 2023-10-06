from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserRegistrationViewTestCase(TestCase):
    def setUp(self) -> None:
        self.path = reverse("users:user-create")
        self.data = {
            "username": "try",
            "email": "em@gmail.com",
            "phone": "+380971112345",
            "password1": "test 1234",
            "password2": "test 1234",
        }

    def test_user_registration_get(self) -> None:
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/user_form.html")

    def test_user_registration_post_success(self) -> None:
        username = self.data["username"]

        self.assertFalse(
            get_user_model().objects.filter(username=username).exists()
        )

        response = self.client.post(self.path, data=self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(
            get_user_model().objects.filter(username=username).exists()
        )

        # check creating of email verification(without using celery)
        # email_verification = EmailVerification.objects.filter(
        #     user__username=username
        # )

        # self.assertTrue(email_verification.exists())
        # self.assertEqual(
        #     email_verification.first().expiration.date(),
        #     (now() + timedelta(hours=48)).date(),
        # )

    def test_user_registration_post_username_error(self) -> None:
        get_user_model().objects.create(username=self.data["username"])
        response = self.client.post(self.path, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "A user with that username already exists.", html=True
        )

    def test_user_registration_post_phone_error(self) -> None:
        self.data["phone"] = "+995579888459"
        response = self.client.post(self.path, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response,
            "Incorrect phone number. Example: +380971234567.",
            html=True,
        )

