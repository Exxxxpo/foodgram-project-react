from rest_framework.pagination import PageNumberPagination


class PaginationForRecipe(PageNumberPagination):
    """Пагинатор для вьюсета RecipeViewSet."""

    page_size_query_param = "limit"
