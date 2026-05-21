from rest_framework import serializers
from .models import DocumentStatusHistory

class DocumentStatusHistorySerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(
        source='document_version.document.title',
        read_only=True
    )
    document_version_number = serializers.IntegerField(
        source='document_version.version_number',
        read_only=True
    )
    changed_by_user = serializers.CharField(
        source='changed_by.user',
        read_only=True
    )
    changed_by_action = serializers.CharField(
        source='changed_by.action',
        read_only=True
    )

    class Meta:
        model = DocumentStatusHistory
        fields = [
            'id',
            'document_version',
            'document_title',
            'document_version_number',
            'old_status',
            'new_status',
            'changed_by',
            'changed_by_user',
            'changed_by_action',
            'changed_at',
        ]
        read_only_fields = '__all__'