from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Document Service API',
        default_version='v1',
        description='API для управления документами и версиями',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def home(request):
    return HttpResponse('''
        <h1>Document Service API</h1>
        <p>Сервер работает!</p>
        <ul>
            <li><a href='/admin/'>Админка</a></li>
            <li><a href='/swagger/'>Swagger документация</a></li>
        </ul>
    ''')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/documents/', include('core.document.urls')),
    path('api/versions/', include('core.document_version.urls')),
    path('api/external/', include('core.external_system.urls')),
    path('api/reports/', include('core.reports.urls')),
    path('api/audit/', include('core.audit_log.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)