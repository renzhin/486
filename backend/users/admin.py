from django.contrib import admin
from django.contrib.auth.models import Group

from .models import ModifiedUser

admin.site.unregister(Group)


@admin.register(ModifiedUser)
class ModifiedUserAdmin(admin.ModelAdmin):
    pass
