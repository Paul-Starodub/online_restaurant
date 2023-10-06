from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from dishes.admin import BasketAdmin, DishAdmin
from dishes.models import Basket, Dish


class DishAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.admin_site = AdminSite()
        self.dish_admin = DishAdmin(Dish, self.admin_site)

    def test_search_fields(self) -> None:
        self.assertEqual(self.dish_admin.search_fields, ("name",))

    def test_list_display_links(self) -> None:
        self.assertEqual(self.dish_admin.list_display_links, ("name",))

    def test_list_display(self) -> None:
        self.assertEqual(
            self.dish_admin.list_display, ("name", "price", "dish_type")
        )

    def test_list_filter(self) -> None:
        self.assertEqual(self.dish_admin.list_filter, ["dish_type"])


class BasketAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.admin_site = AdminSite()
        self.basket_admin = BasketAdmin(Basket, self.admin_site)

    def test_model(self) -> None:
        self.assertEqual(self.basket_admin.model, Basket)

    def test_fields(self) -> None:
        self.assertEqual(
            self.basket_admin.fields, ("dish", "quantity", "created")
        )

    def test_readonly_fields(self) -> None:
        self.assertEqual(self.basket_admin.readonly_fields, ("created",))

    def test_extra(self) -> None:
        self.assertEqual(self.basket_admin.extra, 0)
