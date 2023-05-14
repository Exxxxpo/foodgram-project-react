from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name="tags__slug"
    )
    is_favorited = filters.BooleanFilter(method="filter_for_favorite")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_for_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
        )

    def filter_for_favorite(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipe.objects.filter(favorite_recipe__user=user)
        return Recipe.objects.all()

    def filter_for_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipe.objects.filter(shopping_recipe__user=user)
        return Recipe.objects.all()
