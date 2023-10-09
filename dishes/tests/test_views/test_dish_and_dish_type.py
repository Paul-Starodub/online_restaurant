import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from dishes.forms import DishCustomizeForm
from dishes.models import Dish, DishType

DISHES_URL = reverse("cuisine:dish-list")
DISH_TYPES_URL = reverse("cuisine:dish_type-list")


class PublicDishTypeAndDishTests(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(name="test777")
        self.dish = Dish.objects.create(
            name="test12345",
            description="About task",
            price="20.87",
            image="image.jpg",
            dish_type=self.dish_type,
            stripe_product_price_id="789yohkb",
        )

    def test_dish_list_login_required(self) -> None:
        response = self.client.get(DISHES_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_dish_create_login_required(self) -> None:
        response = self.client.get(reverse("cuisine:dish-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_dish_update_login_required(self) -> None:
        response = self.client.get(
            reverse("cuisine:dish-update", kwargs={"pk": self.dish.id})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_dish_delete_login_required(self) -> None:
        response = self.client.get(
            reverse("cuisine:dish-delete", kwargs={"pk": self.dish.id})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_dish_type_list_login_required(self) -> None:
        response = self.client.get(DISH_TYPES_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_dish_type_create_login_required(self) -> None:
        response = self.client.get(reverse("cuisine:dish_type-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_dish_type_update_login_required(self) -> None:
        response = self.client.get(
            reverse(
                "cuisine:dish_type-update", kwargs={"pk": self.dish_type.id}
            )
        )

        self.assertNotEqual(response.status_code, 200)

    def test_dish_type_delete_login_required(self) -> None:
        response = self.client.get(
            reverse(
                "cuisine:dish_type-delete", kwargs={"pk": self.dish_type.id}
            )
        )

        self.assertNotEqual(response.status_code, 200)


@override_settings(MEDIA_ROOT="/tmp/media")
class PrivateDishTypeAndDishTests(TestCase):
    def setUp(self) -> None:
        image_stream = io.BytesIO()
        image = Image.new("RGB", (100, 100), "white")
        image.save(image_stream, format="JPEG")

        self.image_file = SimpleUploadedFile(
            "test_image.jpg", image_stream.getvalue()
        )
        self.dish_type = DishType.objects.create(name="test777")
        self.dish = Dish.objects.create(
            name="test12345",
            description="About task",
            price="20.87",
            image=self.image_file,
            dish_type=self.dish_type,
            stripe_product_price_id="789yohkb",
        )

        number_of_dishes = 12

        for num in range(2, number_of_dishes):
            dish_type = DishType.objects.create(name=f"{num}type")

            Dish.objects.create(
                name=f"test12345{num}",
                description=f"About task{num}",
                price=f"{num}.27",
                image=self.image_file,
                dish_type=dish_type,
                stripe_product_price_id="789yohkb",
            )

        self.queryset1 = DishType.objects.all()
        self.queryset2 = Dish.objects.all()

        self.user = get_user_model().objects.create_user(
            username="user",
            password="password",
            email="red@gmail.com",
        )
        self.client.force_login(self.user)

    def test_dish_list_login_required(self) -> None:
        response = self.client.get(DISHES_URL)

        self.assertEqual(response.status_code, 200)

    def test_dish_detail_login_required(self) -> None:
        response = self.client.get(
            reverse("cuisine:dish-detail", kwargs={"pk": self.dish.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_dish_create_staff_required(self) -> None:
        form_data = {
            "name": "Test Dish#",
            "description": "Description",
            "image": self.image_file,
            "dish_type": self.dish_type.id,
        }

        response = self.client.post(
            reverse("cuisine:dish-create"), data=form_data
        )

        self.assertNotEqual(response.status_code, 200)

        self.client.logout()
        self.staff = get_user_model().objects.create_user(
            username="staff_user",
            password="password",
            is_staff=True,
            email="ad@gmail.com",
        )
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse("cuisine:dish-create"), data=form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "price", "This field is required."
        )

    def test_dish_update_staff_required(self) -> None:
        form_data = {
            "price": 11.22,
        }
        response = self.client.put(
            reverse("cuisine:dish-update", kwargs={"pk": self.dish.id}),
            data=form_data,
        )

        self.assertNotEqual(response.status_code, 200)

    def test_task_delete_staff_required(self) -> None:
        response = self.client.get(
            reverse("cuisine:dish-delete", kwargs={"pk": self.dish.id})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_retrieve_dishes(self) -> None:
        response = self.client.get(DISHES_URL)
        dish_types = DishType.objects.all()
        dishes = Dish.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.queryset1), list(dish_types))
        self.assertEqual(list(self.queryset2), list(dishes))
        self.assertTemplateUsed(response, "dishes/dishes_list.html")

    def test_pagination_is_ten(self) -> None:
        response = self.client.get(DISHES_URL)

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context_data["dish_list"]), 5)

    def test_dish_customize_form(self) -> None:
        image_stream = io.BytesIO()
        image = Image.new("RGB", (100, 100), "white")
        image.save(image_stream, format="JPEG")
        image_file = SimpleUploadedFile(
            "test_image.jpg", image_stream.getvalue()
        )
        form_data = {
            "name": "Test Dish#",
            "description": "Description",
            "price": 9.99,
            "image": image_file,
            "dish_type": self.dish_type.id,
            "stripe_product_price_id": "789yohkb",
        }
        form = DishCustomizeForm(data=form_data, files=form_data)

        self.assertTrue(form.is_valid())

    def test_search_dish_form(self) -> None:
        response = self.client.get(reverse("cuisine:dish-list") + "?name=user")

        self.assertContains(response, "user")
        self.assertNotContains(response, "Paul")

    def test_dish_type_create_staff_required(self) -> None:
        form_data = {
            "name": "Test# Dish Type",
        }

        response = self.client.post(
            reverse("cuisine:dish_type-create"), data=form_data
        )

        self.assertEqual(response.status_code, 302)

        self.client.logout()
        self.staff = get_user_model().objects.create_user(
            username="staff_user#",
            password="password",
            is_staff=True,
            email="ad1@gmail.com",
        )
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("cuisine:dish_type-create"), data=form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)

    def test_dish_type_update_staff_required(self) -> None:
        form_data = {
            "name": "green",
        }

        response = self.client.put(
            reverse(
                "cuisine:dish_type-update", kwargs={"pk": self.dish_type.id}
            ),
            data=form_data,
        )

        self.assertNotEqual(response.status_code, 200)

        self.client.logout()
        self.staff = get_user_model().objects.create_user(
            username="staff_user#",
            password="password",
            is_staff=True,
            email="ad@gmail.com",
        )
        self.client.force_login(self.staff)

        response = self.client.put(
            reverse(
                "cuisine:dish_type-update", kwargs={"pk": self.dish_type.id}
            ),
            data=form_data,
        )

        self.assertEqual(response.status_code, 200)
