from rest_framework import serializers
from .models import DocumentAccess


class DocumentAccessSerializer(serializers.ModelSerializer):

    document_title = serializers.CharField(source='document.title', read_only=True)
    external_system_name = serializers.CharField(source='external_system.name', read_only=True)

    class Meta:
        model = DocumentAccess
        fields = [
            'id',
            'document',
            'document_title',
            'external_system',
            'external_system_name',
            'created_at'
        ]
        read_only_fields = '__all__'