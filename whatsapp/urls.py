from django.urls import path
from . import views

app_name = 'whats'

urlpatterns = [
    path('', views.message, name='home-whatsapp'),
    path('relatorios/', views.relatorio_whats, name='relatorios_whatsapp'),
    
]
