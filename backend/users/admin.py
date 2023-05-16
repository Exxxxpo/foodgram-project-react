from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "email",
        "username",
        "first_name",
        "last_name",
        "password",
    )
    list_editable = ("password",)
    list_filter = ("is_superuser",)
    search_fields = ("username", "email")
    empty_value_display = "Пусто"


@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    list_editable = ("user", "author")
    empty_value_display = "Пусто"
