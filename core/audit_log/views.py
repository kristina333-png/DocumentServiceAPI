from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(APIView):
    """Просмотр аудита с фильтрацией (только администратор)"""

    permission_classes = [IsAdminUser]

    def get(self, request) -> Response:
        queryset = AuditLog.objects.all()

        document_id = request.query_params.get('document_id')
        if document_id:
            queryset = queryset.filter(document_id=document_id)

        external_system = request.query_params.get('external_system')
        if external_system:
            queryset = queryset.filter(external_system__icontains=external_system)

        action = request.query_params.get('action')
        if action:
            queryset = queryset.filter(action=action)

        date_from = request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)

        date_to = request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)

        serializer = AuditLogSerializer(queryset, many=True)
        return Response(serializer.data)