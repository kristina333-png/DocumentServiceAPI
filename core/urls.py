from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger настройка с поддержкой API-ключа
schema_view = get_schema_view(
    openapi.Info(
        title="Document Service API",
        default_version='v1',
        description="API для управления документами и версиями",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Добавляем схему безопасности для API-ключа
api_key_scheme = openapi.Parameter(
    'X-API-Key',
    openapi.IN_HEADER,
    description="API ключ для аутентификации внешних систем",
    type=openapi.TYPE_STRING,
    required=False
)

def home(request) -> HttpResponse:
    """
    Главная страница сервера.

    Returns:
        HttpResponse: HTML-страница со ссылками на основные разделы
    """
    return HttpResponse("""
        <h1>Документ Service API</h1>
        <p>Сервер работает!</p>
        <ul>
            <li><a href='/admin/'>Админка</a></li>
            <li><a href='/api/documents/'>API документов</a></li>
            <li><a href='/swagger/'>Swagger документация</a></li>
        </ul>
    """)


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    # API маршруты
    path('api/documents/', include('core.document.urls')),
    path('api/versions/', include('core.document_version.urls')),
    path('api/external/', include('core.external_system.urls')),
    path('api/reports/', include('core.reports.urls')),

    # Swagger документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)