from django.contrib.auth import get_user_model
from django.db import models

from cpu_backend.constants import (
    NAME_LONG_NUMBCHAR,
    NAME_SHORT_NUMBCHAR,
)

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        abstract = True


class Vendor(BaseModel):
    """
    Считаю данную модель необходимой
    для возможности массового переименования
    единиц измерений. Например г. в грм.
    """
    name = models.CharField(
        max_length=NAME_SHORT_NUMBCHAR,
        verbose_name='тип',
    )

    class Meta:
        verbose_name = 'вендор'
        verbose_name_plural = 'Вендоры'

    def __str__(self):
        return self.name


class Cpu(BaseModel):
    name = models.CharField(
        max_length=NAME_LONG_NUMBCHAR,
        verbose_name='название',
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        verbose_name='вендор',
    )

    class Meta:
        verbose_name = 'процессор'
        verbose_name_plural = 'Процессоры'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'name',
                    'vendor'
                ),
                name='uniq_cpu'
            ),
        )

    def __str__(self):
        return self.name
