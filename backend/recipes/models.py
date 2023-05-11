from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
# from users.models import User
User = get_user_model()


class Tag(models.Model):
    name = models.TextField(verbose_name='Название', unique=True, blank=False, )
    color = models.CharField(verbose_name='Цветовой HEX код', unique=True, blank=False,
                             max_length=7, validators=[
            RegexValidator(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')])
    slug = models.SlugField(verbose_name='Слаг', unique=True, blank=False, max_length=25)


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингридиент', blank=False, max_length=100)
    measurement_unit = models.TextField(verbose_name='Единицы измерения', blank=False,
                                        max_length=2)


class Recipe(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название', blank=False, max_length=100)
    image = models.ImageField(verbose_name='Изображение', upload_to='recipes/images/', blank=False)
    text = models.CharField(verbose_name='Описание', blank=False, max_length=200)
    ingredients = models.ManyToManyField(Ingredient, verbose_name='Ингридиенты',
                                         through='RecipeIngredient',
                                         through_fields=(
                                         'recipe', 'ingredient'))
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', blank=False)
    cookings_time = models.TimeField(verbose_name='Время приготовления', blank=False)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, verbose_name='Ингридиент',
                                   on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Количество', blank=False)