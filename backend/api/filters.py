from django.db.models import BooleanField, Case, Exists, OuterRef, Value, When
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")
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

    def apply_annotations(self, queryset):
        return queryset.annotate(
            is_favorited=Case(
                When(
                    Exists(
                        self.request.user.favorite_user.filter(
                            recipe=OuterRef('pk')
                        )
                    ),
                    then=Value(True),
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            is_in_shopping_cart=Case(
                When(
                    Exists(
                        self.request.user.shopping_user.filter(
                            recipe=OuterRef('pk')
                        )
                    ),
                    then=Value(True),
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )

    def filter_for_favorite(self, queryset, name, value):
        user = self.request.user
        if value:
            return self.apply_annotations(
                queryset.filter(favorite_recipe__user=user)
            )
        return self.apply_annotations(queryset)

    def filter_for_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return self.apply_annotations(
                queryset.filter(shopping_recipe__user=user)
            )
        return self.apply_annotations(queryset)
