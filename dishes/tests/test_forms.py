from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from dishes.forms import NameSearchForm, DishCustomizeForm
from dishes.models import DishType


class NameSearchFormTests(TestCase):
    def test_name_search_form(self) -> None:
        form_data = {"name": "Test Dish"}
        form = NameSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_name_search_form_with_empty_name(self) -> None:
        form_data = {"name": ""}
        form = NameSearchForm(data=form_data)

        self.assertTrue(form.is_valid())


class DishCustomizeFormTests(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(name="Main Dish")
        self.image_data = open(
            "dishes/test_image/cake-31c4e877-290e-4e10-a947-79f7cfe1b204.jpg",
            "rb",
        ).read()
        self.image = SimpleUploadedFile(
            "test_image.jpg", self.image_data, content_type="image/jpeg"
        )

    def test_dish_customize_form(self) -> None:
        form_data = {
            "name": "Test Dish",
            "description": "Description",
            "price": 9.99,
            "image": self.image,
            "dish_type": self.dish_type.id,
        }
        form = DishCustomizeForm(data=form_data, files=form_data)

        self.assertTrue(form.is_valid())

    def test_dish_customize_form_with_invalid_price(self) -> None:
        form_data = {
            "name": "Test Dish",
            "description": "Description",
            "price": -1.99,  # Invalid price (negative)
            "image": self.image,
            "dish_type": self.dish_type.id,
        }
        form = DishCustomizeForm(data=form_data)

        self.assertFalse(form.is_valid())
