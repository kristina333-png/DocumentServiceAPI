from django.contrib import admin
from .models import ExternalSystem

@admin.register(ExternalSystem)
class ExternalSystemAdmin(admin.ModelAdmin):
    list_display = (
       'name',
        'api_key',
        'is_active',
        'description',
        'created_at'
    )
    list_filter = ('is_active', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    fieldsets = (
        ('Основная информация', {
            'fields': ( 'name',
                        'api_key',
                        'is_active',
                        'description',)
        }),
        ('Системные поля', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('api_key', 'created_at')
