from __future__ import annotations
import os
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    item = models.ForeignKey("Dish", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "item"]


def dish_image_file_path(instance: Dish, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    from django.utils.text import slugify
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/dishes/", filename)


class Dish(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=False, upload_to=dish_image_file_path)
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="dishes"
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through=Like, related_name="dishes"
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("cuisine:dish-detail", kwargs={"pk": self.pk})
