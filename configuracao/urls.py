from django.urls import path
from . import views

app_name = 'config'

urlpatterns = [
    path("configuracoes/", views.configuracoes_view, name="configuracoes"),
]



