# Тестирование Document Service API

## Быстрый старт

```bash
# Запуск контейнеров
docker-compose up --build -d
```
# Создание администратора
```bash
docker-compose exec app python manage.py createsuperuser
# Логин: admin
# Пароль: admin123
```

# Создание внешней системы (для API-ключа)
```bash
docker-compose exec app python manage.py shell

from core.external_system.models import ExternalSystem
system = ExternalSystem.objects.create(name="Тестовая система", is_active=True)
print(f"API Key: {system.api_key}")
# Выход: exit()
```
# Swagger документация
## Доступ к Swagger
### Откройте в браузере:

```text
http://localhost:8000/swagger/
Авторизация в Swagger
Для работы с API в Swagger необходимо авторизоваться:

Нажмите кнопку Authorize (в правом верхнем углу)

Выберите BasicAuth

Введите:

Username: admin

Password: admin123

Нажмите Authorize

Закройте окно

Важно: Для эндпоинтов /external/* используйте только API-ключ, не Basic Auth!

Как выполнить запрос во внешней системе в Swagger
Найдите эндпоинт GET /api/external/documents/

Нажмите "Try it out"

В поле X-API-Key (в заголовках) вставьте API-ключ

Нажмите "Execute"
```

# Запуск тестов
## В PyCharm:
Откройте папку http_requests

Нажмите зелёную стрелку ▶️ слева от запроса



# Сценарии тестирования
```text
1. Документы
Порядок	Запрос	Что делает
1	11_documents_create_post.http	Создать документ
2	10_documents_list_get.http	Список документов
3	12_documents_detail_get.http	Получить по ID
4	13_documents_update_put.http	Обновить
5	14_documents_delete_delete.http	Удалить
2. Версии
Порядок	Запрос	Статус
1	20_versions_upload_post.http	draft (черновик)
2	23_versions_publish_post.http	active (активная)
3	20_versions_upload_post.http	draft (вторая версия)
4	23_versions_publish_post.http	active (вторая)
5	24_versions_rollback_post.http	откат к версии 1
6	22_versions_active_get.http	Проверить активную
7	25_versions_history_get.http	История статусов
3. Внешняя система
Порядок	Запрос	Аутентификация
1	Создать систему в админке	-
2	30_external_documents_get.http	X-API-Key
3	31_external_download_get.http	X-API-Key
4. Отчёты
Запрос	Результат
50_reports_documents_get.http	CSV файл
Переменные
Перед запуском укажите в файлах http_requests:

http
@documentId = 1
@versionId = 1
@apiKey = ваш_api_ключ_сюда
