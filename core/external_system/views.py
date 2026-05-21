from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from core.audit_log.services import AuditLogService
from core.document_version.models import DocumentVersion
from core.document_version.serializers import DocumentVersionSerializer
from core.external_system.services import GetAvailableDocuments, CheckDocumentAccess


class AvailableDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request)-> Response:
        external_system = request.user

        try:
            service = GetAvailableDocuments(external_system=external_system)
            active_versions = service.execute()
            serializer = DocumentVersionSerializer(active_versions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class DownloadVersionView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, version_id):
        external_system = request.user

        try:
            version = DocumentVersion.objects.get(id=version_id)
        except DocumentVersion.DoesNotExist:
            return Response(
                {"error": f"Версия с id {version_id} не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        if version.status != DocumentVersion.StatusVersion.ACTIVE:
            return Response(
                {"error": "Можно скачивать только активные версии"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            service = CheckDocumentAccess(
                external_system=external_system,
                document=version.document
            )
            has_access = service.execute()
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not has_access:
            return Response(
                {"error": "У вас нет доступа к этому документу"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            audit_service = AuditLogService(
                action='download',
                external_system=external_system,
                document=version.document,
                document_version=version
            )
            audit_service.execute()
        except ValidationError as e:
            print(f"Ошибка аудита: {e}")
        try:
            return FileResponse(
                open(version.file_path, 'rb'),
                filename=version.file_name,
                content_type='application/octet-stream'
            )
        except FileNotFoundError:
            return Response(
                {"error": "Файл не найден на сервере"},
                status=status.HTTP_404_NOT_FOUND
            )