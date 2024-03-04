from django.contrib import admin

from .models import (
    Manufacturer,
    Cpu,
)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(Cpu)
class CpuAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'part_number',
        'work_status',
        'purchase_date',
    )
