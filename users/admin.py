from django.contrib import admin
from django.urls import reverse_lazy
from dishes.admin import BasketAdmin

from users.models import User

admin.site.site_url = reverse_lazy("cuisine:dish-list")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone", "image")
    inlines = (BasketAdmin,)
