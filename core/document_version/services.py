import os
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.db.models import QuerySet

from core.base_services import BaseService
from core.document.models import Document
from core.document_status_history.models import DocumentStatusHistory
from core.document_version.models import DocumentVersion


class VersionCreate(BaseService):
    def __init__(self, document_id, file, uploaded_by):
        self.document_id = document_id
        self.file = file
        self.uploaded_by = uploaded_by

    def _execute(self)-> DocumentVersion:
        try:
            document = Document.objects.get(id=self.document_id)
        except Document.DoesNotExist:
            raise ValidationError(f"Документ с id {self.document_id} не найден")


        if not self.file:
            raise ValidationError("Файл обязателен")

        max_version = DocumentVersion.objects.filter(
            document=document
        ).aggregate(models.Max('version_number'))['version_number__max']

        new_version_number = (max_version or 0) + 1


        file_extension = os.path.splitext(self.file.name)[1]
        new_file_name = f"document_{self.document_id}_v{new_version_number}{file_extension}"
        file_path = f"versions/{new_file_name}"


        saved_path = default_storage.save(file_path, ContentFile(self.file.read()))


        version = DocumentVersion.objects.create(
            document=document,
            version_number=new_version_number,
            file_path=saved_path,
            file_name=self.file.name,
            status=DocumentVersion.StatusVersion.DRAFT,
            uploaded_by=None
        )

        return version


class VersionGet(BaseService):
    def __init__(self, version_id):
        self.version_id = version_id

    def _execute(self)-> DocumentVersion:
        try:
            version = DocumentVersion.objects.get(id=self.version_id)
            return version
        except DocumentVersion.DoesNotExist:
            raise ValidationError(f"Версия {self.version_id} не найдена")


class VersionAll(BaseService):
    def __init__(self, document_id):
        self.document_id = document_id

    def _execute(self)-> QuerySet[DocumentVersion]:

        try:
            document = Document.objects.get(id=self.document_id)
        except Document.DoesNotExist:
            raise ValidationError(f"Документ {self.document_id} не найден")


        versions = DocumentVersion.objects.filter(document=document).order_by('-version_number')
        return versions


class VersionGetActive(BaseService):
    def __init__(self, document_id):
        self.document_id = document_id

    def _execute(self)-> DocumentVersion:
        try:
            document = Document.objects.get(id=self.document_id)
        except Document.DoesNotExist:
            raise ValidationError(f"Документ с id {self.document_id} не найден")

        try:
            active_version = DocumentVersion.objects.get(
                document=document,
                status=DocumentVersion.StatusVersion.ACTIVE
            )
            return active_version
        except DocumentVersion.DoesNotExist:
            raise ValidationError(f"У документа {self.document_id} нет активной версии")



class VersionPublish(BaseService):

    def __init__(self, version_id, uploaded_by):
        self.version_id = version_id
        self.uploaded_by = uploaded_by

    def _execute(self)-> DocumentVersion:
        try:
            version = DocumentVersion.objects.get(id=self.version_id)
        except DocumentVersion.DoesNotExist:
            raise ValidationError(f"Версия с id {self.version_id} не найдена")

        if version.status != DocumentVersion.StatusVersion.DRAFT:
            raise ValidationError("Опубликовать можно только черновик.")

        current_active = DocumentVersion.objects.filter(
            document=version.document,
            status=DocumentVersion.StatusVersion.ACTIVE
        ).first()

        if current_active:
            old_status = current_active.status
            current_active.status = DocumentVersion.StatusVersion.ARCHIVED
            current_active.save()

            DocumentStatusHistory.objects.create(
                document_version=current_active,
                old_status=old_status,
                new_status=DocumentVersion.StatusVersion.ARCHIVED,
                changed_by=self.uploaded_by
            )

        old_status = version.status
        version.status = DocumentVersion.StatusVersion.ACTIVE
        version.save()

        DocumentStatusHistory.objects.create(
            document_version=version,
            old_status=old_status,
            new_status=DocumentVersion.StatusVersion.ACTIVE,
            changed_by=self.uploaded_by
        )

        return version

class VersionRollback(BaseService):

    def __init__(self, version_id, uploaded_by):
        self.version_id = version_id
        self.uploaded_by = uploaded_by

    def _execute(self)-> DocumentVersion:
        try:
            target_version = DocumentVersion.objects.get(id=self.version_id)
        except DocumentVersion.DoesNotExist:
            raise ValidationError(f"Версия с id {self.version_id} не найдена")

        if target_version.status != DocumentVersion.StatusVersion.ARCHIVED:
            raise ValidationError("Откат возможен только к архивной версии.")

        current_active = DocumentVersion.objects.filter(
            document=target_version.document,
            status=DocumentVersion.StatusVersion.ACTIVE
        ).first()

        if current_active:
            old_status = current_active.status
            current_active.status = DocumentVersion.StatusVersion.ARCHIVED
            current_active.save()

            DocumentStatusHistory.objects.create(
                document_version=current_active,
                old_status=old_status,
                new_status=DocumentVersion.StatusVersion.ARCHIVED,
                changed_by=self.uploaded_by
            )

        old_status = target_version.status
        target_version.status = DocumentVersion.StatusVersion.ACTIVE
        target_version.save()

        DocumentStatusHistory.objects.create(
            document_version=target_version,
            old_status=old_status,
            new_status=DocumentVersion.StatusVersion.ACTIVE,
            changed_by=self.uploaded_by
        )

        return target_version


