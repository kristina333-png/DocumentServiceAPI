from rest_framework import serializers
from .models import ExternalSystem

class ExternalSystemSerializer(serializers.ModelSerializer):
    """
       Сериализатор для модели ExternalSystem.
       Преобразует объекты ExternalSystem в JSON и обратно.
       """

    class Meta:
        model = ExternalSystem
        fields ='__all__'
        read_only_fields = [
            'created_at',
            'api_key'
        ]