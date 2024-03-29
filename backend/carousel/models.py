from django.db import models

from cpu_backend.constants import (
    NAME_LONG_NUMBCHAR,
)


class Carousel(models.Model):

    name = models.CharField(
        max_length=NAME_LONG_NUMBCHAR,
        verbose_name='название',
    )
    banner = models.ImageField(
        upload_to='carousel/',
        verbose_name='изображение',
    )

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return f'Баннер {self.name}'
