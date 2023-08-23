from django.contrib import admin

from dishes.models import DishType, Dish

admin.site.register(DishType)
admin.site.register(Dish)
