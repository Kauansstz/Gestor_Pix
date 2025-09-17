from django.urls import path
from . import views

app_name = 'pix'

urlpatterns = [
    path('', views.listar_pix, name='listar_pix'),
    path('gerar/', views.gerar_pix, name='gerar_pix'),
]
