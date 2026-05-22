# Document Service API

REST API сервис для управления документами и версиями.

---

## Возможности

- CRUD документов
- Загрузка версий с автоматической нумерацией
- Публикация (черновик → активная)
- Откат к архивным версиям
- Аутентификация внешних систем по API-ключу
- Аудит действий
- CSV-отчёты
- Swagger документация

---

## Стек

| Технология | Версия |
|------------|--------|
| Python | 3.11 |
| Django | 5.2 |
| DRF | 3.17 |
| PostgreSQL | 15 |

---

## Установка

```bash
git clone <repository-url>
cd Documents

python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # Linux/Mac

pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Запуск в Docker
```bash
cp .env.example .env
docker-compose up --build
docker-compose exec app python manage.py createsuperuser

Остановка: docker-compose down
```
## API Эндпоинты
```text
Базовый URL: http://127.0.0.1:8000/api/

Документы:
GET    /documents/              - список (все)
POST   /documents/              - создать (админ)
GET    /documents/{id}/         - просмотр (все)
PUT    /documents/{id}/         - обновить (админ)
DELETE /documents/{id}/         - удалить (админ)

Версии:
POST   /versions/upload/{id}/   - загрузить (админ)
GET    /versions/document/{id}/ - список версий (все)
GET    /versions/document/{id}/active/ - активная (все)
POST   /versions/{id}/publish/  - опубликовать (админ)
POST   /versions/{id}/rollback/ - откат (админ)

Внешние системы (с API-ключом):
GET /external/documents/        - доступные документы
GET /external/download/{id}/    - скачать файл

Отчёты (только админ):
GET /reports/documents/         - CSV по документам
GET /reports/systems/           - CSV по системам

Документация:
/swagger/  - Swagger
/admin/    - Админка
```
## Структура проекта
```text
Documents/                                 # Корень проекта
│
├── docker-compose.yml                     # Docker оркестрация
├── Dockerfile                             # Docker образ
├── manage.py                              # Django управление
├── requirements.txt                       # Зависимости
├── .env                                   # Переменные окружения
│
├── http_requests/                         # HTTP тесты (PyCharm)
│   ├── 00_home_get.http
│   ├── 11_documents_create_post.http
│   ├── 20_versions_upload_post.http
│   ├── 23_versions_publish_post.http
│   ├── 30_external_documents_get.http
│   └── 31_external_download_get.http
│
├── media/                                 # Загруженные файлы
│   └── versions/
│
└── core/                                  # Основной код
    │
    ├── settings.py                        # Настройки Django
    ├── urls.py                            # Главные маршруты
    ├── base_services.py                   # Базовый сервис (транзакции)
    │
    ├── document/                          #  Документы
    │   ├── models.py                      # Document
    │   ├── views.py                       # CRUD документов
    │   ├── services.py                    # Бизнес-логика
    │   └── urls.py
    │
    ├── document_version/                  #  Версии
    │   ├── models.py                      # DocumentVersion (draft/active/archived)
    │   ├── views.py                       # Загрузка, публикация, откат
    │   ├── services.py                    # Логика версий
    │   └── urls.py
    │
    ├── document_access/                   #  Доступ
    │   └── models.py                      # DocumentAccess (связь документ ↔ система)
    │
    ├── document_status_history/           #  История статусов
    │   ├── models.py                      # DocumentStatusHistory
    │   └── serializers.py
    │
    ├── external_system/                   #  Внешние системы
    │   ├── models.py                      # ExternalSystem (api_key)
    │   ├── authentication.py              # APIKeyAuthentication
    │   ├── views.py                       # Доступные документы, скачивание
    │   ├── services.py                    # Проверка доступа
    │   └── urls.py
    │
    ├── audit_log/                         #  Аудит
    │   ├── models.py                      # AuditLog (действия)
    │   └── services.py                    # Логирование
    │
    └── reports/                           #  Отчёты
        ├── views.py                       # CSV отчёты
        └── services.py                    # Формирование отчётов
```
