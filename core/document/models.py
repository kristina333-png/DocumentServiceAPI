from django.db import models


class Document(models.Model):
    """
        Модель документа (карточка нормативно-справочного материала).
        """

    class DocumentType(models.TextChoices):
        REGULATION = 'regulation', 'Регламент'
        METHODOLOGICAL_RECOMMENDATIONS = 'methodological_recommendations', 'Методические рекомендации'

    title = models.CharField(
        null=False,
        db_index=True,
        max_length=160,
        verbose_name="Название документа"
    )
    description = models.TextField(
        null=True,
        max_length=500,
        blank=True,
        verbose_name="Описание"
    )
    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices,
        default=DocumentType.REGULATION,
        db_index=True,
        verbose_name="Тип документа"
    )
    is_common = models.BooleanField(
        default=True,
        verbose_name="Общий документ"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title


