from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.TextField(
        verbose_name="Название", unique=True, max_length=200
    )
    color = models.CharField(
        verbose_name="Цветовой HEX код",
        unique=True,
        max_length=7,
        validators=[RegexValidator(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")],
    )
    slug = models.SlugField(verbose_name="Слаг", unique=True, max_length=200)

    class Meta:
        ordering = ["-id"]


class Ingredient(models.Model):
    name = models.CharField(verbose_name="Ингридиент", max_length=200)
    measurement_unit = models.TextField(
        verbose_name="Единицы измерения", max_length=200
    )

    class Meta:
        ordering = ["-id"]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    name = models.CharField(verbose_name="Название", max_length=200)
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="recipes/",
    )
    text = models.CharField(verbose_name="Описание", max_length=1000)
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингридиенты",
        through="RecipeIngredient",
        through_fields=("recipe", "ingredient"),
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тэги",
    )
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления", validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ["-id"]


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
    amount = models.IntegerField(
        verbose_name="Количество", validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ["-id"]


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
        unique_together = ("user", "recipe")
        ordering = ["-id"]


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
        unique_together = ("user", "recipe")
        ordering = ["-id"]
