from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from dishes.models import Basket
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

    def update_after_payment(self) -> None:
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.STATUSES[1][0]
        self.basket_history = {
            "purchased_items": [basket.de_json() for basket in baskets],
            "total_sum": float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
