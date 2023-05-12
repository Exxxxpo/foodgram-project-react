from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # ADMIN = 'admin'
    # USER = 'user'
    # ROLES = (
    #     (USER, 'Пользователь'),
    #     (ADMIN, 'Администратор'),
    # )
    email = models.EmailField('Электронная почта', unique=True, max_length=254, blank=False)
    # first_name = models.CharField('Имя', max_length=150, blank=False)
    # last_name = models.CharField('Фамилия', max_length=150, blank=False)
    # role = models.CharField('Роль', max_length=25, choices=ROLES, default=USER)

    class Meta:
        ordering = ('pk',)

    # @property
    # def is_admin(self):
    #     return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.username

class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=False,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        unique_together = ('user', 'author')
