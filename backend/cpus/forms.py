from django import forms
from django.core.mail import send_mail
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

    def clean(self):
        """
        Тестовая отправка писем админу
        при добавлении процессора
        """
        super().clean()
        user = self.cleaned_data['user']
        part_number = self.cleaned_data['part_number']
        send_mail(
            subject='Добавление процессора на сайт 486.renzhin.ru',
            message=f'{user} добавил процессор {part_number}',
            from_email='noreplay@486.renzhin.ru',
            recipient_list=['admin@486.renzhin.ru'],
            fail_silently=True,
        )
