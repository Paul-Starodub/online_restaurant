import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from dishes.forms import DishCustomizeForm, NameSearchForm
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
        image_stream = io.BytesIO()
        image = Image.new("RGB", (100, 100), "white")
        image.save(image_stream, format="JPEG")
        self.image_file = SimpleUploadedFile(
            "test_image.jpg", image_stream.getvalue()
        )

    def test_dish_customize_form(self) -> None:
        form_data = {
            "name": "Test Dish",
            "description": "Description",
            "price": 9.99,
            "image": self.image_file,
            "dish_type": self.dish_type.id,
        }

        form = DishCustomizeForm(data=form_data, files=form_data)

        self.assertTrue(form.is_valid())

    def test_dish_customize_form_with_invalid_price(self) -> None:
        form_data = {
            "name": "Test Dish#",
            "description": "Description",
            "price": -1.99,
            "image": self.image_file,
            "dish_type": self.dish_type.id,
        }
        form = DishCustomizeForm(data=form_data, files=form_data)

        self.assertFalse(form.is_valid())
