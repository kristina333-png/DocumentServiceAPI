from django.db import models


class DocumentVersion(models.Model):
    """
      Модель версии документа.
      Содержит файл и статус версии (черновик, активная, архивная).
      """
    class StatusVersion(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        ACTIVE = 'active', 'Активная'
        ARCHIVED = 'archived', 'Архивная'

    document = models.ForeignKey(
        'document.Document',
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name="Документ"
    )
    version_number = models.PositiveIntegerField(
        default=1,
        verbose_name="Номер версии"
    )
    file_path = models.CharField(
        max_length=260,
        verbose_name="Путь до сохранённого файла"
    )
    file_name = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name="Исходное имя файла"
    )
    status = models.CharField(
        max_length=50,
        choices=StatusVersion.choices,
        default=StatusVersion.DRAFT,
        verbose_name="Статус версии"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки"
    )
    uploaded_by = models.ForeignKey(
         'audit_log.AuditLog',
         on_delete=models.SET_NULL,
         null=True,
        verbose_name="Пользователь, загрузивший версию"
    )

    class Meta:
        verbose_name = "Версия документа"
        verbose_name_plural = "Версии документов"
        unique_together = [['document', 'version_number']]
        ordering = ['-version_number']

    def __str__(self)-> str:
        return f"{self.document.title} - v{self.version_number}"

