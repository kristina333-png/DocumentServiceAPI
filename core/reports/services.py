from typing import List, Dict, Any

from django.db.models import Count
from core.base_services import BaseService
from core.audit_log.models import AuditLog


class DocumentDownloadReport(BaseService):
    """
        Сервис формирования отчёта по скачиваниям документов.
        Группирует записи аудита по документам и считает количество скачиваний.
        """

    def _execute(self)-> List[Dict[str, Any]]:
        report_data = AuditLog.objects.filter(
            action=AuditLog.Action.FILE_DOWNLOADED
        ).values(
            'document_id',
            'document__title'
        ).annotate(
            download_count=Count('id')
        ).order_by('-download_count')

        result = []
        for item in report_data:
            result.append({
                'document_id': item['document_id'],
                'title': item['document__title'],
                'download_count': item['download_count']
            })

        return result


class SystemDownloadReport(BaseService):
    """
     Сервис формирования отчёта по скачиваниям внешних систем.
     Группирует записи аудита по внешним системам и считает количество скачиваний.
     """
    def _execute(self)-> List[Dict[str, Any]]:
        report_data = AuditLog.objects.filter(
            action=AuditLog.Action.FILE_DOWNLOADED
        ).exclude(
            external_system__isnull=True
        ).exclude(
            external_system=''
        ).values(
            'external_system'
        ).annotate(
            download_count=Count('id')
        ).order_by('-download_count')

        result = []
        for item in report_data:
            result.append({
                'system_name': item['external_system'],
                'download_count': item['download_count']
            })

        return result