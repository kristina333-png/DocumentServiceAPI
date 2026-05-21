from django.contrib import admin
from .models import DocumentStatusHistory

@admin.register(DocumentStatusHistory)
class DocumentStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
       'document_version',
        'old_status',
        'new_status',
        'changed_by',
        'changed_at'
    )

    fieldsets = (
        ('Основная информация', {
            'fields': ('document_version',
                       'old_status',
                       'new_status',
                       'changed_by')
        }),
        ('Системные поля', {
            'fields': ('changed_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('document_version',
                       'old_status',
                       'new_status',
                       'changed_by',
                       'changed_at')