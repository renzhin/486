from django.contrib.auth.models import AbstractUser
from django.db import models

from cpus.validators import username_validator
from cpu_backend.constants import USER_FIELDS_NUMBCHAR


def user_directory_path(instance, filename):
    """
    Функция для генерации пути сохранения изображения аватары.
    Файл будет загружен в MEDIA_ROOT/user_<id>/<filename>
    """
    return 'user_{0}/{1}'.format(
        instance.id,
        filename
    )


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
        verbose_name='Фамилия',
    )
    password = models.CharField(
        max_length=USER_FIELDS_NUMBCHAR,
        verbose_name='Пароль',
    )
    avatar = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        verbose_name='Аватар',
    )
    registrated_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата регистрации',
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
