from rest_framework import serializers
from .models import DocumentStatusHistory

class DocumentStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentStatusHistory
        fields = '__all__'
        read_only_fields = ('id', 'changed_at')
