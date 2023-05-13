from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

# from users.models import User
User = get_user_model()


class Tag(models.Model):
    name = models.TextField(
        verbose_name="Название",
        unique=True,
        blank=False,
    )
    color = models.CharField(
        verbose_name="Цветовой HEX код",
        unique=True,
        blank=False,
        max_length=7,
        validators=[RegexValidator(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")],
    )
    slug = models.SlugField(
        verbose_name="Слаг", unique=True, blank=False, max_length=25
    )


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Ингридиент", blank=False, max_length=100
    )
    measurement_unit = models.TextField(
        verbose_name="Единицы измерения", blank=False, max_length=2
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    name = models.CharField(
        verbose_name="Название", blank=False, max_length=100
    )
    image = models.ImageField(
        verbose_name="Изображение", upload_to="recipes/", blank=False
    )
    text = models.CharField(
        verbose_name="Описание", blank=False, max_length=200
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингридиенты",
        through="RecipeIngredient",
        through_fields=("recipe", "ingredient"),
    )
    tags = models.ManyToManyField(Tag, verbose_name="Тэги", blank=False)
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления", blank=False
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингридиент",
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    amount = models.IntegerField(verbose_name="Количество", blank=False)


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_user",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite_recipe",
        verbose_name="Избранный рецепт",
    )

    class Meta:
        verbose_name = "Избранные рецепты"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite"
            )
        ]


class Shopping_cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_user",
        verbose_name="Пользователь, который добавил в корзину",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_recipe",
        verbose_name="Рецепт добавленный в корзину",
    )

    class Meta:
        verbose_name = "Корзина"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_cart"
            )
        ]
