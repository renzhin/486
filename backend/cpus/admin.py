from django.contrib import admin

from .models import (
    Manufacturer,
    Cpu,
    ImageCpu
)


class ImageCpuInline(admin.TabularInline):
    model = ImageCpu
    extra = 1


@admin.register(Cpu)
class CpuAdmin(admin.ModelAdmin):
    inlines = [ImageCpuInline]
    list_display = (
        'part_number',
        'catalog_number',
        'work_status',
        'purchase_date',
    )
    readonly_fields = ('catalog_number',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass
