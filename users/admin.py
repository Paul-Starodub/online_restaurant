from django.contrib import admin
from django.urls import reverse_lazy

from users.models import User

admin.site.site_url = reverse_lazy("cuisine:dish-list")
admin.site.register(User)
