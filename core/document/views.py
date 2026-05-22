from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
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

    @swagger_auto_schema(
        operation_description="Получить список всех документов с фильтрацией",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY,
                              description="Поиск по названию", type=openapi.TYPE_STRING),
            openapi.Parameter('document_type', openapi.IN_QUERY,
                              description="Тип документа", type=openapi.TYPE_STRING),
        ],
        responses={200: DocumentSerializer(many=True)}
    )
    def get(self, request) -> Response:
        search = request.query_params.get('search', '')
        doc_type = request.query_params.get('document_type', '')

        service = DocumentAll()
        documents = service.execute()

        if search:
            documents = documents.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        if doc_type:
            documents = documents.filter(document_type=doc_type)

        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Создать новый документ (только администратор)",
        request_body=DocumentSerializer,
        responses={201: DocumentSerializer()}
    )
    def post(self, request) -> Response:
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

    @swagger_auto_schema(
        operation_description="Получить документ по ID",
        responses={200: DocumentSerializer()}
    )
    def get(self, request, pk) -> Response:
        try:
            service = DocumentGet(document_id=pk)
            document = service.execute()
            serializer = DocumentSerializer(document)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Обновить документ (только администратор)",
        request_body=DocumentSerializer,
        responses={200: DocumentSerializer()}
    )
    def put(self, request, pk) -> Response:
        try:
            service = DocumentUpdate(
                document_id=pk,
                title_new=request.data.get('title'),
                description_new=request.data.get('description'),
                document_type_new=request.data.get('document_type'),
                is_common_new=request.data.get('is_common')
            )
            document = service.execute()
            serializer = DocumentSerializer(document)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Удалить документ (только администратор)",
        responses={200: "Документ удален"}
    )
    def delete(self, request, pk) -> Response:
        try:
            service = DocumentDelete(document_id=pk)
            result = service.execute()
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)