from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from dishes.admin import BasketAdmin
from users.models import EmailVerification, User

admin.site.site_url = reverse_lazy("cuisine:dish-list")
admin.site.site_header = "Restaurant admin panel"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone", "get_html_photo")
    inlines = (BasketAdmin,)

    def get_html_photo(self, object_: User) -> str:
        if object_.image:
            return mark_safe(f"<img src='{object_.image.url}' width=50>")

    get_html_photo.short_description = "photo_mini"


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "expiration")
    fields = ("code", "user", "expiration", "created")
    readonly_fields = ("created",)
