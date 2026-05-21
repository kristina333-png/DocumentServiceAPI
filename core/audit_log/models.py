from django.db import models


class AuditLog(models.Model):
    """
     Модель аудита действий.
     Фиксирует скачивания файлов, выдачу и отзыв доступа.
     """
    class Action(models.TextChoices):
        FILE_DOWNLOADED = 'file_downloaded', 'Скачивание файла документа'
        ACCESS_GRANTED = 'access_granted', 'Выдача доступа к документу'
        ACCESS_REVOKED = 'access_revoked', 'Отзыв доступа'

    user = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Администратор"
    )

    external_system = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Внешняя система"
    )

    document = models.ForeignKey(
        'document.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Документ"
    )

    document_version = models.ForeignKey(
        'document_version.DocumentVersion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Версия документа"
    )

    action = models.CharField(
        max_length=50,
        choices=Action.choices,
        default=Action.FILE_DOWNLOADED,
        verbose_name="Действие"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время действия"
    )

    metadata = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Дополнительная информация"
    )

    class Meta:
        verbose_name = "Запись аудита"
        verbose_name_plural = "Записи аудита"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"AuditLog #{self.pk} - {self.action}"