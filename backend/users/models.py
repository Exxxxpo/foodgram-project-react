from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        "Электронная почта",
        unique=True,
        max_length=254,
    )
    password = models.CharField('Пароль', max_length=150)

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=False,
        related_name="subscribing",
        verbose_name="Автор",
    )

    class Meta:
        unique_together = ("user", "author")
