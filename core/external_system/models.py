import secrets

from django.db import models


class ExternalSystem(models.Model):
    """
      Модель внешней системы.
      Хранит API-ключ для аутентификации и информацию о системе.
      """

    name = models.CharField(
        max_length=260,
        verbose_name="Название внешней системы"
    )
    api_key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Ключ доступа к API",
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Внешняя система"
        verbose_name_plural = "Внешние системы"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name