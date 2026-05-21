from django.urls import path
from . import views

urlpatterns = [
    # Список доступных документов
    path('documents/', views.AvailableDocumentsView.as_view(), name='available-documents'),

    # Скачивание файла
    path('download/<int:version_id>/', views.DownloadVersionView.as_view(), name='download-version'),
]