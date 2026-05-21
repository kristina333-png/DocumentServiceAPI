from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'external_system',
        'action',
        'document',
        'document_version',
        'created_at',
    )

    list_filter = (
        'action',
        'created_at',
    )

    list_select_related = ('document', 'document_version')

    search_fields = ('user', 'external_system', 'metadata')

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'user',
                'external_system',
                'action',
                'document',
                'document_version',
                'metadata')
        }),
        ('Системные поля', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = (
        'user', 'external_system', 'document',
        'document_version', 'action', 'created_at', 'metadata'
    )



    list_per_page = 25