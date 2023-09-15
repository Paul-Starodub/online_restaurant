from django.contrib import admin

from dishes.models import DishType, Dish, Basket


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display_links = ("name",)
    list_display = ["id", "name", "price", "dish_type"]
    list_filter = ["dish_type"]


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ("dish", "quantity", "created")
    readonly_fields = ("created",)
    extra = 0


admin.site.register(DishType)
