
from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentListCreateView.as_view(), name='document_list'),
    path('<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
]