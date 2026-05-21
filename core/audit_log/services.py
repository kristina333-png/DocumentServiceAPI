from django.core.exceptions import ValidationError
from core.base_services import BaseService

from core.audit_log.models import AuditLog


class AuditLogService(BaseService):

    def __init__(self, action, **kwargs):
        self.action = action
        self.kwargs = kwargs

    def _execute(self)-> AuditLog:
        if self.action == 'download':
            return self._log_download(
                external_system=self.kwargs.get('external_system'),
                document=self.kwargs.get('document'),
                document_version=self.kwargs.get('document_version')
            )

        elif self.action == 'access_granted':
            return self._log_access_granted(
                admin_user=self.kwargs.get('admin_user'),
                document=self.kwargs.get('document'),
                external_system=self.kwargs.get('external_system')
            )

        elif self.action == 'access_revoked':
            return self._log_access_revoked(
                admin_user=self.kwargs.get('admin_user'),
                document=self.kwargs.get('document'),
                external_system=self.kwargs.get('external_system')
            )

        else:
            raise ValidationError(f"Неизвестное действие аудита: {self.action}")

    def _log_download(self, external_system, document, document_version)-> AuditLog:
        if not external_system:
            raise ValidationError("Внешняя система не указана")
        if not document:
            raise ValidationError("Документ не указан")
        if not document_version:
            raise ValidationError("Версия документа не указана")

        return AuditLog.objects.create(
            external_system=external_system.name,
            document=document,
            document_version=document_version,
            action=AuditLog.Action.FILE_DOWNLOADED,
            metadata=f"Скачан файл {document_version.file_name} системой {external_system.name}"
        )

    def _log_access_granted(self, admin_user, document, external_system)-> AuditLog:
        if not admin_user:
            raise ValidationError("Администратор не указан")
        if not document:
            raise ValidationError("Документ не указан")
        if not external_system:
            raise ValidationError("Внешняя система не указана")

        admin_name = admin_user if isinstance(admin_user, str) else admin_user.username

        return AuditLog.objects.create(
            user=admin_name,
            external_system=external_system.name,
            document=document,
            action=AuditLog.Action.ACCESS_GRANTED,
            metadata=f"Выдан доступ к документу '{document.title}' системе {external_system.name}"
        )

    def _log_access_revoked(self, admin_user, document, external_system)-> AuditLog:
        if not admin_user:
            raise ValidationError("Администратор не указан")
        if not document:
            raise ValidationError("Документ не указан")
        if not external_system:
            raise ValidationError("Внешняя система не указана")

        admin_name = admin_user if isinstance(admin_user, str) else admin_user.username

        return AuditLog.objects.create(
            user=admin_name,
            external_system=external_system.name,
            document=document,
            action=AuditLog.Action.ACCESS_REVOKED,
            metadata=f"Отозван доступ к документу '{document.title}' у системы {external_system.name}"
        )