from django.contrib import admin
from . import models


@admin.register(models.Telegram)
class TelegramAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')
    readonly_fields = ('id', 'username', 'first_name', 'last_name')
    search_fields = ('__all__',)
