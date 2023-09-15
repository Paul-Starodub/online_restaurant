from __future__ import annotations
import os
import uuid
from _decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.db.models import F, Sum


class DishType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


def dish_image_file_path(instance: Dish, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    from django.utils.text import slugify

    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/dishes/", filename)


class Dish(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(limit_value=0)],
    )
    image = models.ImageField(null=False, upload_to=dish_image_file_path)
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="dishes"
    )
    likes = models.ManyToManyField(
        get_user_model(), related_name="dishes", blank=True
    )

    class Meta:
        verbose_name_plural = "dishes"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("cuisine:dish-detail", kwargs={"pk": self.pk})


class BasketQuerySet(models.QuerySet):
    def total_sum(self) -> Decimal:
        result = self.aggregate(
            total_sum=Sum(
                F("dish__price") * F("quantity"),
                output_field=models.DecimalField(
                    max_digits=15, decimal_places=2
                ),
            )
        )
        return result["total_sum"]

    def total_quantity(self) -> int:
        result = self.aggregate(total_quantity=Sum("quantity"))
        return result["total_quantity"]


class Basket(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="baskets"
    )
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name="baskets"
    )
    quantity = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self) -> str:
        return f"Basket for user {self.user} | Dish: {self.dish}"

    @property
    def sum(self) -> Decimal:
        return self.dish.price * self.quantity
