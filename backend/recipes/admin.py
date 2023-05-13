from django.contrib import admin

from . import models


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    list_filter = ("name",)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    list_editable = ("name", "color", "slug")
    list_filter = ("pk", )
    empty_value_display = "Пусто"


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "name", "image", "cooking_time")
    list_editable = ("cooking_time",)
    readonly_fields = ("in_favorites",)
    list_filter = ("name", "author", "tags")
    search_fields = ("name", "author")
    empty_value_display = "Пусто"

    @admin.display(description="В избранном")
    def in_favorites(self, obj):
        return obj.favorite_recipe.count()


@admin.register(models.RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "ingredient", "amount")
    list_editable = ("recipe", "ingredient", "amount")


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    list_editable = ("user", "recipe")


@admin.register(models.Shopping_cart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    list_editable = ("user", "recipe")
