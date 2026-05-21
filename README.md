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


## Запуск в Docker

cp .env.example .env
docker-compose up --build
docker-compose exec app python manage.py createsuperuser

Остановка: docker-compose down

## API Эндпоинты

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

## Получение API-ключа

В админке: /admin/external_system/externalsystem/add/
Создайте систему и скопируйте ключ.

Использование: заголовок X-API-Key: ваш-ключ

## Статусы версий

draft    - черновик
active   - активная
archived - архивная

## Структура проекта

Documents/
├── core/
│   ├── document/
│   ├── document_version/
│   ├── external_system/
│   ├── audit_log/
│   └── reports/
├── media/
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py

