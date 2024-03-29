from django.contrib import admin

from .models import Carousel


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    pass
