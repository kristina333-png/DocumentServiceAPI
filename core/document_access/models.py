from django.db import models


class DocumentAccess(models.Model):
    document = models.ForeignKey(
        'document.Document',
        on_delete=models.CASCADE,
        related_name='allowed_systems',
        verbose_name="Документ"
    )

    external_system = models.ForeignKey(
        'external_system.ExternalSystem',
        on_delete=models.CASCADE,
        related_name='accessible_documents',
        verbose_name="Внешняя система"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата выдачи"
    )

    class Meta:
        verbose_name = "Доступ документа"
        verbose_name_plural = "Доступы документов"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.document} -> {self.external_system}"