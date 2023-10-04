from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

from users.models import validate_ukrainian_phone_number


class Order(models.Model):
    STATUSES = (
        (0, "created"),
        (1, "paid"),
        (2, "on_way"),
        (3, "delivered"),
    )
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    phone = PhoneNumberField(
        region="UA",
        validators=[
            validate_ukrainian_phone_number,
        ],
    )
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=0, choices=STATUSES)
    initiator = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self) -> str:
        return f"Order #{self.id}. {self.first_name} {self.last_name}"
