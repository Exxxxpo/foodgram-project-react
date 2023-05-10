from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.TextField('Название', unique=True, blank=False, )
    color = models.CharField('Цветовой HEX код', unique=True, blank=False,
                             max_length=7, validators=[
            RegexValidator(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')])
    slug = models.SlugField('Слаг', unique=True, blank=False, max_length=25)
