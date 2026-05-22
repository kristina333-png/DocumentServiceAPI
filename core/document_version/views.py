from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from core.document_version.serializers import DocumentVersionSerializer
from core.document_version.services import VersionCreate, VersionAll, VersionGetActive, VersionPublish, VersionRollback


class VersionUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_description="Загрузить новую версию документа (только администратор)",
        manual_parameters=[
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Файл документа",
                required=True,
            ),
        ],
        responses={
            201: DocumentVersionSerializer(),
            400: "Ошибка валидации",
            404: "Документ не найден"
        }
    )
    def post(self, request, document_id) -> Response:
        try:
            file = request.FILES.get('file')

            if not file:
                return Response(
                    {"error": "Файл не передан"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            service = VersionCreate(
                document_id=document_id,
                file=file,
                uploaded_by=request.user
            )
            version = service.execute()
            serializer = DocumentVersionSerializer(version)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class VersionListView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    @swagger_auto_schema(
        operation_description="Получить список всех версий документа",
        responses={200: DocumentVersionSerializer(many=True)}
    )
    def get(self, request, document_id) -> Response:
        try:
            service = VersionAll(document_id)
            versions = service.execute()
            serializer = DocumentVersionSerializer(versions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )


class ActiveVersionView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    @swagger_auto_schema(
        operation_description="Получить активную версию документа",
        responses={200: DocumentVersionSerializer()}
    )
    def get(self, request, document_id) -> Response:
        try:
            service = VersionGetActive(document_id)
            active_version = service.execute()
            serializer = DocumentVersionSerializer(active_version)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )


class VersionPublishView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Опубликовать версию (черновик → активная) - только администратор",
        responses={200: "Версия опубликована"}
    )
    def post(self, request, version_id) -> Response:
        try:
            service = VersionPublish(
                version_id=version_id,
                uploaded_by=request.user
            )
            version = service.execute()
            serializer = DocumentVersionSerializer(version)

            return Response(
                {
                    "message": f"Версия {version.version_number} успешно опубликована",
                    "version": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class VersionRollbackView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Откатить документ к архивной версии - только администратор",
        responses={200: "Откат выполнен"}
    )
    def post(self, request, version_id) -> Response:
        try:
            service = VersionRollback(
                version_id=version_id,
                uploaded_by=request.user
            )
            version = service.execute()
            serializer = DocumentVersionSerializer(version)

            return Response(
                {
                    "message": f"Документ откачен к версии {version.version_number}",
                    "version": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class VersionHistoryView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Получить историю изменения статусов версии",
        responses={200: "Список изменений статусов"}
    )
    def get(self, request, version_id) -> Response:
        from core.document_status_history.models import DocumentStatusHistory
        from core.document_status_history.serializers import DocumentStatusHistorySerializer

        try:
            history = DocumentStatusHistory.objects.filter(
                document_version_id=version_id
            ).order_by('-changed_at')

            if not history.exists():
                return Response(
                    {"message": "История статусов для этой версии не найдена"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = DocumentStatusHistorySerializer(history, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )