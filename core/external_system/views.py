from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.exceptions import ValidationError
import os
from django.conf import settings

from core.audit_log.services import AuditLogService
from core.document.models import Document
from core.document_access.models import DocumentAccess
from core.document_access.serializers import DocumentAccessSerializer
from core.document_version.models import DocumentVersion
from core.document_version.serializers import DocumentVersionSerializer
from core.external_system.models import ExternalSystem
from core.external_system.services import GetAvailableDocuments, CheckDocumentAccess


api_key_param = openapi.Parameter(
    'X-API-Key',
    openapi.IN_HEADER,
    description="API ключ внешней системы (получите в админке)",
    type=openapi.TYPE_STRING,
    required=True
)


class AvailableDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список активных версий документов, доступных внешней системе",
        manual_parameters=[api_key_param],
        responses={200: DocumentVersionSerializer(many=True)}
    )
    def get(self, request) -> Response:
        external_system = request.user

        if not external_system.is_active:
            return Response(
                {"error": "Внешняя система деактивирована"},
                status=status.HTTP_403_FORBIDDEN
            )

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

    @swagger_auto_schema(
        operation_description="Скачать файл версии документа (только активные версии)",
        manual_parameters=[api_key_param],
        responses={200: "Файл", 403: "Доступ запрещён", 404: "Не найден"}
    )
    def get(self, request, version_id):
        external_system = request.user

        if not external_system.is_active:
            return Response(
                {"error": "Внешняя система деактивирована"},
                status=status.HTTP_403_FORBIDDEN
            )

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
            file_full_path = os.path.join(settings.MEDIA_ROOT, version.file_path)
            return FileResponse(
                open(file_full_path, 'rb'),
                filename=version.file_name,
                content_type='application/octet-stream'
            )
        except FileNotFoundError:
            return Response(
                {"error": f"Файл не найден: {version.file_path}"},
                status=status.HTTP_404_NOT_FOUND
            )


class GrantAccessView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Выдать доступ внешней системе к документу (только администратор)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'document_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID документа'),
                'external_system_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID внешней системы'),
            },
            required=['document_id', 'external_system_id']
        ),
        responses={201: DocumentAccessSerializer()}
    )
    def post(self, request) -> Response:
        document_id = request.data.get('document_id')
        external_system_id = request.data.get('external_system_id')

        if not document_id or not external_system_id:
            return Response(
                {"error": "document_id и external_system_id обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            document = Document.objects.get(id=document_id)
            external_system = ExternalSystem.objects.get(id=external_system_id)
        except Document.DoesNotExist:
            return Response(
                {"error": "Документ не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        except ExternalSystem.DoesNotExist:
            return Response(
                {"error": "Внешняя система не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        if document.is_common:
            return Response(
                {"warning": "Документ является общим, доступ уже есть у всех систем"},
                status=status.HTTP_200_OK
            )

        access, created = DocumentAccess.objects.get_or_create(
            document=document,
            external_system=external_system
        )

        if created:
            audit_service = AuditLogService(
                action='access_granted',
                admin_user=request.user.username,
                document=document,
                external_system=external_system
            )
            audit_service.execute()

            serializer = DocumentAccessSerializer(access)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": "Доступ уже предоставлен"},
                status=status.HTTP_200_OK
            )


class RevokeAccessView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Отозвать доступ внешней системы к документу (только администратор)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'document_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID документа'),
                'external_system_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID внешней системы'),
            },
            required=['document_id', 'external_system_id']
        ),
        responses={200: "Доступ отозван"}
    )
    def post(self, request) -> Response:
        document_id = request.data.get('document_id')
        external_system_id = request.data.get('external_system_id')

        if not document_id or not external_system_id:
            return Response(
                {"error": "document_id и external_system_id обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            access = DocumentAccess.objects.get(
                document_id=document_id,
                external_system_id=external_system_id
            )
        except DocumentAccess.DoesNotExist:
            return Response(
                {"error": "Доступ не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        document = access.document
        external_system = access.external_system

        if document.is_common:
            return Response(
                {"error": "У общего документа нельзя отозвать доступ"},
                status=status.HTTP_400_BAD_REQUEST
            )

        access.delete()
        audit_service = AuditLogService(
            action='access_revoked',
            admin_user=request.user.username,
            document=document,
            external_system=external_system
        )
        audit_service.execute()

        return Response(
            {"message": "Доступ отозван"},
            status=status.HTTP_200_OK
        )