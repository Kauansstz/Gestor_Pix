from django.contrib import admin
from django.urls import path, include

from django.shortcuts import redirect

def home(request):
    return redirect('usuarios:login')  # nome da URL de login que você definiu em usuarios/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('vendas/', include('vendas.urls')),
    path('pix/', include('pix.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('', home, name='home'),
]

