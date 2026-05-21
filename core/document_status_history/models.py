from django.db import models


class DocumentStatusHistory(models.Model):

    document_version = models.ForeignKey(
        'document_version.DocumentVersion',
        on_delete=models.CASCADE,
        related_name='status_history',
        verbose_name="Версия документа"
    )

    old_status = models.CharField(
        max_length=50,
        verbose_name="Предыдущий статус версии"
    )

    new_status = models.CharField(
        max_length=50,
        verbose_name="Новый статус версии"
    )

    changed_by = models.ForeignKey(
        'audit_log.AuditLog',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь, изменивший статус"
    )

    changed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата изменения"
    )

    class Meta:
        verbose_name = "История изменения статуса"
        verbose_name_plural = "Истории изменения статусов"
        ordering = ['-changed_at']


    def __str__(self):
        return f"{self.document_version} - {self.old_status} → {self.new_status} - {self.changed_at}"