from django.contrib.auth.models import AbstractUser
from django.db import models

from cpus.validators import username_validator
from cpu_backend.constants import USER_FIELDS_NUMBCHAR


class ModifiedUser(AbstractUser):

    email = models.EmailField(
        unique=True,
        max_length=USER_FIELDS_NUMBCHAR,
        verbose_name='Электронная почта',
    )
    username = models.CharField(
        max_length=USER_FIELDS_NUMBCHAR,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[username_validator]
    )
    first_name = models.CharField(
        max_length=USER_FIELDS_NUMBCHAR,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=USER_FIELDS_NUMBCHAR,
        blank=True,
        verbose_name='Фамилия',
    )
    password = models.CharField(
        max_length=USER_FIELDS_NUMBCHAR,
        verbose_name='Пароль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name'
    )
    USERNAME_FIELD = 'email'
