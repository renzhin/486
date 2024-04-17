from django import forms


class CpuForm(forms.Form):
    part_number = forms.CharField()
    description = forms.CharField()

    purchase_date = forms.DateField()
    sale_date = forms.DateField()
