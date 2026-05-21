from django.db import transaction


class BaseService:
    """
        Базовый класс для всех сервисов проекта.
        Обеспечивает автоматическое выполнение в транзакции базы данных.

        """
    @transaction.atomic
    def execute(self):
        return self._execute()

    def _execute(self):
        raise NotImplementedError("Ты забыл переопределить метод _execute")