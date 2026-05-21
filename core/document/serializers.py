from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели Document.
        Преобразует обекты Document в JSON и обратно
        """
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']