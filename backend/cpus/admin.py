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
    pass
