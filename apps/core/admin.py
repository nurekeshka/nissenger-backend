from django.contrib import admin

from . import models


@admin.register(models.Version)
class VersionAdmin(admin.ModelAdmin):
    fields = ('major', 'minor', 'patch')
    list_display = ('major', 'minor', 'patch')
    ordering = ('-major', '-minor', '-patch')
