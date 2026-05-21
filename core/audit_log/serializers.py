from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    """
       Сериализатор для модели AuditLog.
       Преобразует объекты AuditLog в JSON и обратно.
       """
    document_title = serializers.CharField(source='document.title', read_only=True)
    document_version_number = serializers.IntegerField(
        source='document_version.version_number',
        read_only=True
    )

    class Meta:
        model = AuditLog
        fields = [
            'id',
            'user',
            'external_system',
            'document',
            'document_title',
            'document_version',
            'document_version_number',
            'action',
            'created_at',
            'metadata'
        ]
        read_only_fields = '__all__'