from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.listar_relatorios, name='listar_relatorios'),
    path('<int:pk>/', views.relatorio_detail, name='detail'),
    path('exportar/', views.exportar_csv, name='exportar_csv'),
        path('novo/', views.criar_relatorio, name='criar_relatorio'),

]
