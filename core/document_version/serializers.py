from rest_framework import serializers
from .models import DocumentVersion


class DocumentVersionSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source='document.title', read_only=True)
    uploaded_by_user = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = DocumentVersion
        fields = (
            'id', 'document', 'document_title', 'version_number',
            'file_path', 'file_name', 'status', 'status_display',
            'uploaded_at', 'uploaded_by', 'uploaded_by_user'
        )
        read_only_fields = ('id', 'document_title', 'version_number', 'status_display', 'uploaded_at')

    def get_uploaded_by_user(self, obj):
        if obj.uploaded_by:
            return obj.uploaded_by.username
        return None