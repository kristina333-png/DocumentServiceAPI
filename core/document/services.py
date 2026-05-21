from typing import Dict, Any

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from core.base_services import BaseService
from core.document.models import Document

class DocumentCreate(BaseService):
    """
       Сервис создания нового документа.
       """

    def __init__(self, title, description, document_type, is_common=False):
        self.title = title
        self.description = description
        self.document_type = document_type
        self.is_common = is_common

    def _execute(self)-> Document:
        errors = []
        if not self.title:
            errors.append("Название обязательно")
        if not self.description:
            errors.append("Описание обязательно")

        if errors:
            raise ValidationError(errors)

        return Document.objects.create(
            title=self.title,
            description=self.description,
            document_type=self.document_type,
            is_common=self.is_common
        )


class DocumentGet(BaseService):
    """
       Сервис получения документа по ID.
       """
    def __init__(self, document_id):
        self.document_id = document_id

    def _execute(self)-> Document:
        try:
            return Document.objects.get(id=self.document_id)
        except Document.DoesNotExist:
            raise ValidationError(f"Документ с id {self.document_id} не найден")


class DocumentAll(BaseService):
    """
     Сервис получения всех документов.
     """
    def _execute(self)-> QuerySet[Document]:
        return Document.objects.all()


class DocumentUpdate(BaseService):
    """
    Сервис обновления документа.
    """
    def __init__(self, document_id, title_new=None, description_new=None,
                 document_type_new=None, is_common_new=None):
        self.document_id = document_id
        self.title_new = title_new
        self.description_new = description_new
        self.document_type_new = document_type_new
        self.is_common_new = is_common_new

    def _execute(self)-> Document:
        try:
            document = Document.objects.get(id=self.document_id)
        except Document.DoesNotExist:
            raise ValidationError(f"Документ с id {self.document_id} не найден")

        if self.title_new is not None:
            document.title = self.title_new

        if self.description_new is not None:
            document.description = self.description_new

        if self.document_type_new is not None:
            document.document_type = self.document_type_new

        if self.is_common_new is not None:
            document.is_common = self.is_common_new

        document.save()
        return document


class DocumentDelete(BaseService):
    """
     Сервис удаления документа.
     """
    def __init__(self, document_id):
        self.document_id = document_id

    def _execute(self)-> Dict[str, Any]:
        try:
            document = Document.objects.get(id=self.document_id)
        except Document.DoesNotExist:
            raise ValidationError(f"Документ с id {self.document_id} не найден")

        if document.versions.exists():
            raise ValidationError("Нельзя удалить документ, у которого есть версии")

        document.delete()
        return {"message": f"Документ {self.document_id} удален", "id": self.document_id}