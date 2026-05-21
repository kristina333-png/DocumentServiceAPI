from django.urls import path
from .views import (
    VersionUploadView,
    VersionListView,
    ActiveVersionView,
    VersionPublishView,
    VersionRollbackView,
)

urlpatterns = [
    # Загрузка новой версии (POST)
    path('upload/<int:document_id>/', VersionUploadView.as_view(), name='version-upload'),

    # Список всех версий документа (GET)
    path('document/<int:document_id>/', VersionListView.as_view(), name='version-list'),

    # Активная версия документа (GET)
    path('document/<int:document_id>/active/', ActiveVersionView.as_view(), name='version-active'),

    # Публикация версии (POST)
    path('<int:version_id>/publish/', VersionPublishView.as_view(), name='version-publish'),

    # Откат версии (POST)
    path('<int:version_id>/rollback/', VersionRollbackView.as_view(), name='version-rollback'),
]