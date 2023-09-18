from django.contrib import admin

from blog.models import Post, Commentary


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("description",)
    list_display = ("description", "user", "dish")
    list_filter = ("dish__dish_type",)
    ordering = ("-created_time",)


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    search_fields = ("post__dish__name",)
    list_display = ("content", "user", "post")
