from typing import List

from core.base_services import BaseService
from core.document.models import Document
from core.document_access.models import DocumentAccess
from core.document_version.models import DocumentVersion


class GetAvailableDocuments(BaseService):
    """
      Сервис получения списка активных версий документов,
      доступных внешней системе.
      """
    def __init__(self, external_system):
        self.external_system = external_system

    def _execute(self)-> List[DocumentVersion]:
        common_documents = Document.objects.filter(is_common=True)
        accessed_documents = Document.objects.filter(
            allowed_systems__external_system=self.external_system
        )

        all_documents = common_documents.union(accessed_documents)

        active_versions = []
        for document in all_documents:
            try:
                active_version = DocumentVersion.objects.get(
                    document=document,
                    status=DocumentVersion.StatusVersion.ACTIVE
                )
                active_versions.append(active_version)
            except DocumentVersion.DoesNotExist:

                continue

        return active_versions


class CheckDocumentAccess(BaseService):
    def __init__(self, external_system, document):
        self.external_system = external_system
        self.document = document

    def _execute(self) -> bool:
        if self.document.is_common:
            return True

        return DocumentAccess.objects.filter(
            document=self.document,
            external_system=self.external_system
        ).exists()