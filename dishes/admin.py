from django.contrib import admin

from dishes.models import DishType, Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display_links = ("name",)
    list_display = ["id", "name", "price", "dish_type"]
    list_filter = ["dish_type"]


admin.site.register(DishType)
