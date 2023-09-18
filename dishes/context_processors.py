from django.http import HttpRequest
from django.db.models import QuerySet
from dishes.models import Basket


def baskets(request: HttpRequest) -> QuerySet[Basket] | list:
    user = request.user
    return {
        "baskets": Basket.objects.filter(user=user)
        if user.is_authenticated
        else []
    }
