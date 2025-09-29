from django.urls import path
from . import views

app_name = 'whats'

urlpatterns = [
    path('', views.message, name='home-whatsapp'),
    path('relatorios/', views.relatorio_whats, name='relatorios_whatsapp'),
    path('exportar/relatorio', views.exportar_csv_relatorio, name='exportar_csv_relaroio'),
    path('exportar/cliente', views.exportar_csv_list_client, name='exportar_csv_list_client'),
    path('client/listar_clientes', views.list_client, name='list_whatsapp'),
    path('client/new_client', views.new_client, name='new_client'),
]
