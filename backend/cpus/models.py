from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
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

    name = models.CharField(
        max_length=NAME_LONG_NUMBCHAR,
        verbose_name='название',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    work_status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=NOTEST,
        verbose_name='Статус'
    )
    rarity = models.CharField(
        max_length=2,
        choices=RARITY_CHOICES,
        default=NONE,
        verbose_name='Редкость'
    )
    part_number = models.CharField(
        max_length=NAME_SHORT_NUMBCHAR,
        verbose_name='серийный номер',
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
    overclk_frequency = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='частота в разгоне',
        blank=True,
        null=True,
    )
    fsb = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='частота шины',
        blank=True,
        null=True,
    )
    overclk_fsb = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='частота шины в разгоне',
        blank=True,
        null=True,
    )
    multiplier = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='множитель',
        blank=True,
        null=True,
    )
    overclk_multiplier = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='множитель в разгоне',
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
    overclk_vcore = models.FloatField(
        validators=[MinValueValidator(1)],
        verbose_name='напряжение ядра в разгоне',
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cpus',
        verbose_name='Владелец'
    )
    purchase_date = models.DateTimeField(
        verbose_name='дата покупки'
    )
    purchase_price = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Стоимость покупки',
        blank=True,
        null=True,
    )
    sale_price = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Стоимость продажи',
        blank=True,
        null=True,
    )
    price_description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание покупки/продажи'
    )
    image = models.ImageField(
        upload_to='cpus/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'процессор'
        verbose_name_plural = 'Процессоры'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'name',
                    'manufacturer'
                ),
                name='uniq_cpu'
            ),
        )

    def __str__(self):
        return self.name
