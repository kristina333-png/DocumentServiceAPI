from django.urls import path
from . import views

urlpatterns = [
    # Отчёт по документам
    path('documents/', views.DocumentReportView.as_view(), name='document-report'),

    # Отчёт по системам
    path('systems/', views.SystemReportView.as_view(), name='system-report'),
]