import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


username_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Буквы, цифры и символы @/./+/-/_',
)


def real_date(date):
    """
    Валидация дата покупки или продажи,
    что она не в будущем
    """
    today = datetime.date.today()
    interval_date = (today - date).days
    if interval_date < 0:
        raise ValidationError(
            'Дата не может быть в будущем'
        )
