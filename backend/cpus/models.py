from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from cpu_backend.constants import (
    NAME_SHORT_NUMBCHAR,
    CHOICE_NUMBCHAR,
)
from cpus.validators import real_date

User = get_user_model()


def user_cpu_directory_path(instance, filename):
    """
    Функция для генерации пути сохранения изображений процессоров.
    Файл будет загружен в MEDIA_ROOT/user_<id>/cpu_<id>/<filename>
    """
    return 'user_{0}/cpu_{1}/{2}'.format(
        instance.cpu.user.id,
        instance.cpu.id,
        filename
    )


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        abstract = True


class Manufacturer(BaseModel):
    """
    Производитель
    """
    name = models.CharField(
        max_length=NAME_SHORT_NUMBCHAR,
        verbose_name='тип',
    )

    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Cpu(BaseModel):
    """
    Процессор
    """
    NOTEST = 'NT'
    WORK = 'WK'
    DEFECTIVE = 'DF'
    OVERCLOCK = 'OC'
    NONE = 'NN'
    COMMON = 'CM'
    UNOCOMMON = 'UN'
    RARE = 'RR'
    EXTRARARE = 'ER'

    RARITY_CHOICES = [
        (NONE, 'Не задано'),
        (COMMON, 'Частый'),
        (UNOCOMMON, 'Нечастый'),
        (RARE, 'Редкий'),
        (EXTRARARE, 'Очень редкий'),
    ]

    STATUS_CHOICES = [
        (NOTEST, 'Непроверенный'),
        (WORK, 'Рабочий'),
        (DEFECTIVE, 'Неисправен'),
        (OVERCLOCK, 'Разогнан'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cpus',
        verbose_name='владелец'
    )
    part_number = models.CharField(
        max_length=NAME_SHORT_NUMBCHAR,
        verbose_name='серийный номер',
    )
    catalog_number = models.CharField(
        max_length=4,
        verbose_name='номер в коллекции',
        blank=True
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='описание'
    )
    hidden_description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Скрытое описание'
    )
    work_status = models.CharField(
        max_length=CHOICE_NUMBCHAR,
        choices=STATUS_CHOICES,
        default=NOTEST,
        verbose_name='статус'
    )
    rarity = models.CharField(
        max_length=CHOICE_NUMBCHAR,
        choices=RARITY_CHOICES,
        default=NONE,
        verbose_name='редкость'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name='cpus',
        verbose_name='производитель',
    )
    family = models.CharField(
        max_length=NAME_SHORT_NUMBCHAR,
        verbose_name='семейство',
    )
    frequency = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='частота процессора',
    )
    fsb = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='частота шины',
        blank=True,
        null=True,
    )
    multiplier = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='множитель',
        blank=True,
        null=True,
    )
    fpu = models.BooleanField(
        default=True,
        verbose_name='математический сопроцессор (FPU)'
    )
    l1_cache_size = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='размер кеша L1',
        blank=True,
        null=True,
    )
    vcore = models.FloatField(
        validators=[MinValueValidator(1)],
        verbose_name='напряжение ядра',
        blank=True,
        null=True,
    )

    overclk_frequency = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='частота в разгоне',
        blank=True,
        null=True,
    )
    overclk_fsb = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='частота шины в разгоне',
        blank=True,
        null=True,
    )
    overclk_multiplier = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='множитель в разгоне',
        blank=True,
        null=True,
    )
    overclk_vcore = models.FloatField(
        validators=[MinValueValidator(1)],
        verbose_name='напряжение ядра в разгоне',
        blank=True,
        null=True,
    )

    purchase_date = models.DateField(
        verbose_name='дата покупки',
        validators=(real_date,)
    )
    purchase_price = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='стоимость покупки',
        blank=True,
        null=True,
    )
    sale_price = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='стоимость продажи',
        blank=True,
        null=True,
    )
    sale_date = models.DateField(
        verbose_name='дата продажи',
        blank=True,
        null=True,
        validators=(real_date,)
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    in_interesting = models.BooleanField(
        default=False,
        verbose_name='В интересном',
        help_text='Снимите галочку, чтобы скрыть с главной.'
    )

    class Meta:
        ordering = ('-purchase_date', '-created_at')
        verbose_name = 'процессор'
        verbose_name_plural = 'Процессоры'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'catalog_number',
                    'user'
                ),
                name='uniq_cpu'
            ),
        )

    def __str__(self):
        return self.part_number

    def get_absolute_url(self):
        return reverse('cpus:cpu_detail', kwargs={'pk': self.pk})


class ImageCpu(models.Model):
    """
    Изображения для процессора
    """
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='название изображения',
    )
    cpu = models.ForeignKey(
        Cpu,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='процессор',
    )
    image = models.ImageField(
        upload_to=user_cpu_directory_path,
        verbose_name='фото процессора',
    )
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Проверяем, есть ли уже у этого процессора изображение с default=True
        existing_default_image = ImageCpu.objects.filter(
            cpu=self.cpu,
            default=True
        ).first()
        if existing_default_image and self.default:
            # Если такое изображение существует и default=True,
            # то сбрасываем default на False у существующего изображения
            existing_default_image.default = False
            existing_default_image.save()
        super().save(*args, **kwargs)
