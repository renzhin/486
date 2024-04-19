from django import forms

from .models import Cpu


class CpuForm(forms.ModelForm):
    # part_number = forms.CharField(
    #     label='Серийный номер*',
    #     max_length=NAME_SHORT_NUMBCHAR
    # )
    # description = forms.CharField(
    #     label='Описание',
    #     required=False
    # )
    work_status = forms.ChoiceField(
        choices=[('', 'Все')] + Cpu.STATUS_CHOICES,
        label='Статус*'
    )
    rarity = forms.ChoiceField(
        choices=[('', 'Все')] + Cpu.RARITY_CHOICES,
        label='Редкость*'
    )
    # manufacturer = forms.CharField(
    #     label='Производитель*'
    # )
    family = forms.CharField(
        label='Семейство*'
    )
    # frequency = forms.IntegerField(
    #     min_value=1,
    #     label='Частота процессора*'
    # )
    # fsb = forms.IntegerField(
    #     required=False,
    #     min_value=1,
    #     label='Частота шины'
    # )
    # multiplier = forms.IntegerField(
    #     required=False,
    #     min_value=1,
    #     label='Множитель'
    # )
    # fpu = forms.BooleanField(
    #     required=False,
    #     label='Сопроцессор (FPU)'
    # )
    # l1_cache_size = forms.IntegerField(
    #     required=False,
    #     min_value=1,
    #     label='Кеш L1'
    # )
    # vcore = forms.FloatField(
    #     required=False,
    #     label='Напряжение ядра'
    # )
    # purchase_date = forms.DateField(
    #     label='Дата покупки*',
    #     widget=forms.DateInput(attrs={'type': 'date'})
    # )
    # purchase_price = forms.IntegerField(
    #     required=False,
    #     min_value=0,
    #     label='Стоимость покупки'
    # )
    # sale_date = forms.DateField(
    #     required=False,
    #     label='Дата продажи',
    #     widget=forms.DateInput(attrs={'type': 'date'})
    # )
    # sale_price = forms.IntegerField(
    #     required=False,
    #     min_value=0,
    #     label='Стоимость продажи'
    # )

    class Meta:
        model = Cpu
        exclude = ('catalog_number',)

        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'sale_date': forms.DateInput(attrs={'type': 'date'})
        }
