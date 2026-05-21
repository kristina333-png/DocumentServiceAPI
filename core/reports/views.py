import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from .services import DocumentDownloadReport, SystemDownloadReport


class DocumentReportView(APIView):
    """
     Эндпоинт для скачивания CSV-отчёта по документам.
     GET: Возвращает CSV-файл с количеством скачиваний каждого документа.
     Только для администратора.
     """
    permission_classes = [IsAdminUser]

    def get(self, request)-> HttpResponse:
        try:
            service = DocumentDownloadReport()
            report_data = service.execute()
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="document_download_report.csv"'}
            )
            writer = csv.writer(response)
            writer.writerow(['document_id', 'title', 'download_count'])

            for row in report_data:
                writer.writerow([
                    row['document_id'],
                    row['title'],
                    row['download_count']
                ])

            return response

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class SystemReportView(APIView):
    """
        Эндпоинт для скачивания CSV-отчёта по внешним системам.
        GET: Возвращает CSV-файл с количеством скачиваний каждой системы.
        Только для администратора.
        """
    permission_classes = [IsAdminUser]

    def get(self, request)-> HttpResponse:
        try:
            service = SystemDownloadReport()
            report_data = service.execute()

            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="system_download_report.csv"'}
            )
            writer = csv.writer(response)
            writer.writerow(['system_name', 'download_count'])

            for row in report_data:
                writer.writerow([
                    row['system_name'],
                    row['download_count']
                ])

            return response
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )