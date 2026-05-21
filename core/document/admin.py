from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'document_type',
        'is_common',
        'created_at',
        'updated_at'
    )

    list_display_links = ('title',)

    list_filter = (
        'document_type',
        'is_common',
        'created_at'
    )

    search_fields = ('title', 'description')

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'document_type', 'is_common')
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25