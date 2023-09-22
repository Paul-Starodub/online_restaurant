from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
from dishes.models import DishType, Dish, Basket


class DishTypesTests(TestCase):
    def test_dish_type_str(self) -> None:
        dish_type = DishType.objects.create(name="Test Type")
        self.assertEqual(str(dish_type), "Test Type")


class DishesTests(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(name="Test Type")
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="Test Description",
            price=Decimal("10.00"),
            dish_type=self.dish_type,
        )

    def test_dish_str(self) -> None:
        self.assertEqual(str(self.dish), self.dish.name)

    def test_absolute_url(self) -> None:
        self.assertEqual(
            self.dish.get_absolute_url(),
            reverse("cuisine:dish-detail", kwargs={"pk": self.dish.id}),
        )


class BasketQuerySetTests(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(name="Test Type")
        self.dish1 = Dish.objects.create(
            name="Dish 1",
            description="Description 1",
            price=Decimal("10.00"),
            dish_type=self.dish_type,
        )
        self.dish2 = Dish.objects.create(
            name="Dish 2",
            description="Description 2",
            price=Decimal("20.00"),
            dish_type=self.dish_type,
        )
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.basket1 = Basket.objects.create(
            user=self.user, dish=self.dish1, quantity=2
        )
        self.basket2 = Basket.objects.create(
            user=self.user, dish=self.dish2, quantity=3
        )

    def test_str_representation(self) -> None:
        expected_str = f"Basket for user {self.user} | Dish: {self.dish1}"
        self.assertEqual(str(self.basket1), expected_str)

    def test_sum_property(self) -> None:
        expected_sum = Decimal("20.00")
        self.assertEqual(self.basket1.sum, expected_sum)

    def test_total_sum(self) -> None:
        total_sum = Basket.objects.total_sum()
        expected_total_sum = Decimal("2") * Decimal("10.00") + Decimal(
            "3"
        ) * Decimal("20.00")
        self.assertEqual(total_sum, expected_total_sum)

    def test_total_quantity(self) -> None:
        total_quantity = Basket.objects.total_quantity()
        expected_total_quantity = 2 + 3
        self.assertEqual(total_quantity, expected_total_quantity)
