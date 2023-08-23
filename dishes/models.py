from django.conf import settings
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=63)

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


class Dish(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="dishes"
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through=Like, related_name="dishes"
    )

    def __str__(self) -> str:
        return self.name
