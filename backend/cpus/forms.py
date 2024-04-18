from django import forms

from cpu_backend.constants import (
    NAME_SHORT_NUMBCHAR,
)


class CpuForm(forms.Form):
    part_number = forms.CharField(max_length=NAME_SHORT_NUMBCHAR)
    # description = forms.CharField(required=False)
    work_status = forms.CharField()
    rarity = forms.CharField()
    manufacturer = forms.CharField()
    family = forms.CharField()
    frequency = forms.PositiveIntegerField()
    # fsb = PositiveIntegerField(required=False)
    # multiplier = PositiveIntegerField(required=False)
    fpu = BooleanField(required=False)
    # l1_cache_size = PositiveIntegerField(required=False)
    # vcore = FloatField(required=False)
    purchase_date = forms.DateField()
    purchase_price = PositiveIntegerField(required=False)
    sale_date = forms.DateField()
    # sale_price = PositiveIntegerField(required=False)
    # sale_date = forms.DateField(required=False)
