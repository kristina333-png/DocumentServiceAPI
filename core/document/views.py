from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from core.document.serializers import DocumentSerializer
from core.document.services import DocumentAll, DocumentCreate, DocumentGet, DocumentUpdate, DocumentDelete


class DocumentListCreateView(APIView):
    """
       Эндпоинт для работы со списком документов.
        GET: Возвращает список всех документов. Доступен всем
    POST: Создаёт новый документ. Только для администратора"""

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request)-> Response:
        service = DocumentAll()
        documents = service.execute()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request)-> Response:
        try:
            service = DocumentCreate(
                title=request.data.get('title'),
                description=request.data.get('description'),
                document_type=request.data.get('document_type'),
                is_common=request.data.get('is_common', False)
            )
            document = service.execute()
            serializer = DocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailView(APIView):
    """
       Эндпоинт для работы с одним документом.

       GET: Возвращает документ по ID. Доступен всем.
       PUT: Обновляет документ. Только для администратора.
       DELETE: Удаляет документ. Только для администратора.
       """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, pk)-> Response:
        try:
            service = DocumentGet(document_id=pk)
            document = service.execute()
            serializer = DocumentSerializer(document)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk)-> Response:
        try:
            service = DocumentUpdate(
                document_id=pk,
                title_new=request.data.get('title_new'),
                description_new=request.data.get('description_new'),
                document_type_new=request.data.get('document_type_new'),
                is_common_new=request.data.get('is_common_new')
            )
            document = service.execute()
            serializer = DocumentSerializer(document)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk)-> Response:
        try:
            service = DocumentDelete(document_id=pk)
            result = service.execute()
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)