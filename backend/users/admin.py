from django.contrib import admin
from django.contrib.auth.models import Group

from .models import ModifiedUser

admin.site.unregister(Group)


@admin.register(ModifiedUser)
class ModifiedUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'get_cpus_count',
    )

    def get_cpus_count(self, obj):
        return obj.cpus.count()

    get_cpus_count.short_description = 'Количество процов'
