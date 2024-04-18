from django import forms

from cpu_backend.constants import (
    NAME_SHORT_NUMBCHAR,
)


class CpuForm(forms.Form):
    part_number = forms.CharField(
        label='Серийный номер*',
        max_length=NAME_SHORT_NUMBCHAR
    )
    description = forms.CharField(
        label='Описание',
        required=False
    )
    work_status = forms.ChoiceField(
        label='Статус*'
    )
    rarity = forms.ChoiceField(
        label='Редкость*'
    )
    manufacturer = forms.CharField(
        label='Производитель*'
    )
    family = forms.CharField(
        label='Семейство*'
    )
    frequency = forms.IntegerField(
        min_value=1,
        label='Частота процессора*'
    )
    fsb = forms.IntegerField(
        required=False,
        min_value=1,
        label='Частота шины'
    )
    multiplier = forms.IntegerField(
        required=False,
        min_value=1,
        label='Множитель'
    )
    fpu = forms.BooleanField(
        required=False,
        label='Сопроцессор (FPU)'
    )
    l1_cache_size = forms.IntegerField(
        required=False,
        min_value=1,
        label='Кеш L1'
    )
    vcore = forms.FloatField(
        required=False,
        label='Напряжение ядра'
    )
    purchase_date = forms.DateField(
        label='Дата покупки*'
    )
    purchase_price = forms.IntegerField(
        required=False,
        min_value=0,
        label='Стоимость покупки'
    )
    sale_date = forms.DateField(
        required=False,
        label='Дата продажи'
    )
    sale_price = forms.IntegerField(
        required=False,
        min_value=0,
        label='Стоимость продажи'
    )
