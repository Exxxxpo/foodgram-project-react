from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers import (IngredientSerializer, RecipeCreateSerializer,
                             RecipeReadSerializer, RecipeSerializer,
                             SetPasswordSerializer, SubscribeAuthorSerializer,
                             SubscriptionsSerializer, TagSerializer,
                             UserCreateSerializer, UserReadSerializer)
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            Shopping_cart, Tag)
from users.models import Subscribe

from .filters import RecipeFilter
from .pagination import PaginationForRecipe
from .permission import AuthorOrReadOnlyPermission

User = get_user_model()


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserReadSerializer
        return UserCreateSerializer

    @action(
        detail=False,
        methods=["get"],
        pagination_class=None,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = UserReadSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False, methods=["post"], permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {"detail": "Пароль изменён!"}, status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs["pk"])

        if request.method == "POST":
            serializer = SubscribeAuthorSerializer(
                author, data=request.data, context={"request": request}
            )
            serializer.is_valid()
            Subscribe.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            get_object_or_404(
                Subscribe, user=request.user, author=author
            ).delete()
            return Response(
                {"detail": "Успешная отписка"},
                status=status.HTTP_204_NO_CONTENT,
            )


class TagViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ["get", "post", "patch", "create", "delete"]
    pagination_class = PaginationForRecipe

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs["pk"])

        if request.method == "POST":
            serializer = RecipeSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid()
            if Favorite.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {"errors": "Рецепт уже в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Favorite.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            get_object_or_404(
                Favorite, user=request.user, recipe=recipe
            ).delete()
            return Response(
                {"detail": "Рецепт успешно удален из избранного."},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=(IsAuthenticated,),
        pagination_class=None,
    )
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get("pk"))

        if request.method == "POST":
            serializer = RecipeSerializer(
                recipe, data=request.data, context={"request": request}
            )
            serializer.is_valid()
            if Shopping_cart.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {"errors": "Рецепт уже в списке покупок."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Shopping_cart.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            get_object_or_404(
                Shopping_cart, user=request.user, recipe=recipe
            ).delete()
            return Response(
                {"detail": "Рецепт успешно удален из списка покупок."},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(
        detail=False, methods=["get"], permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, **kwargs):
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_recipe__user=request.user
            )
            .values("ingredient")
            .annotate(total_amount=Sum("amount"))
            .values_list(
                "ingredient__name",
                "total_amount",
                "ingredient__measurement_unit",
            )
        )
        response_contents = []
        [
            response_contents.append("{} - {} {}.".format(*ingredient))
            for ingredient in ingredients
        ]
        response = HttpResponse(
            "Cписок покупок:\n" + "\n".join(response_contents),
            content_type="text/plain",
        )
        response[
            "Content-Disposition"
        ] = "attachment; filename=shopping_cart.txt"
        return response
