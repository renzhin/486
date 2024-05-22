from django import forms
from django.forms.models import inlineformset_factory

from .models import Cpu, ImageCpu

# Создаем inline-форму для ImageCpu
ImageCpuFormSet = inlineformset_factory(
    Cpu,
    ImageCpu,
    fields=('name', 'image', 'default'),
    extra=3
)


class CpuForm(forms.ModelForm):
    work_status = forms.ChoiceField(
        choices=[('', 'Все')] + Cpu.STATUS_CHOICES,
        label='Статус*',
    )
    rarity = forms.ChoiceField(
        choices=[('', 'Все')] + Cpu.RARITY_CHOICES,
        label='Редкость*'
    )

    class Meta:
        model = Cpu
        exclude = ('catalog_number',)

        widgets = {
            'purchase_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'sale_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            )
        }
