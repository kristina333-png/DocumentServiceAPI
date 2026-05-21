from django.contrib import admin
from .models import DocumentAccess

@admin.register(DocumentAccess)
class DocumentAccessAdmin(admin.ModelAdmin):
    list_display = (
        'document',
        'external_system',
        'created_at'
    )

    list_filter = ('created_at',)

    search_fields = ('document__title', 'external_system__name')

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('document', 'external_system')
        }),
        ('Системные поля', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
