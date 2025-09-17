from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('', views.listar_vendas, name='listar_vendas'),
    path('nova/', views.nova_venda, name='nova_venda'),
]
