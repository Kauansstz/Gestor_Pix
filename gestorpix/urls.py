from django.contrib import admin
from django.urls import path, include

from django.shortcuts import redirect

def home(request):
    return redirect('usuarios:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('vendas/', include('vendas.urls')),
    path('pix/', include('pix.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('whatsapp/', include('whatsapp.urls')),
    path('', home, name='home'),
]

