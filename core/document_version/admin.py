from django.contrib import admin
from .models import DocumentVersion


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = (
        'document',
        'version_number',
        'file_name',
        'status',
        'uploaded_by',
        'uploaded_at',
    )

    list_filter = ('status', 'uploaded_at')

    list_display_links = ('file_name',)

    search_fields = ('document__title', 'file_name')

    list_select_related = ('document', 'uploaded_by')

    readonly_fields = ('document', 'version_number', 'uploaded_at', 'uploaded_by')

    fieldsets = (
        ('Основная информация', {
            'fields': ('document',
                       'version_number',
                       'file_path',
                       'file_name',
                       'status',
                       'uploaded_by')
        }),
        ('Системные поля', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )