from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from core.document_version.serializers import DocumentVersionSerializer
from core.document_version.services import VersionCreate, VersionAll, VersionGetActive, VersionPublish, VersionRollback


class VersionUploadView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    def post(self, request, document_id)-> Response:
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

    def get(self, request, document_id)-> Response:
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

    def get(self, request, document_id)-> Response:
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

    def post(self, request, version_id)-> Response:
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

    def post(self, request, version_id)-> Response:
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