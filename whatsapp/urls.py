from django.urls import path # type: ignore
from . import views

app_name = 'whats'

urlpatterns = [
    path('', views.message, name='home-whatsapp'),
    path('relatorios/', views.relatorio_whats, name='relatorios_whatsapp'),
    path('exportar/relatorio', views.exportar_csv_relatorio, name='exportar_csv_relaroio'),
    path('exportar/cliente', views.exportar_csv_list_client, name='exportar_csv_list_client'),
    path('client/listar_clientes', views.list_client, name='list_whatsapp'),
    path('client/new_client', views.new_client, name='new_client'),
    path("client/importar/", views.import_client, name="importar_clientes"),
    # path("", views.chat_view, name="chat"), Quando api estiver disponivel
    # path("conversas/", views.listar_conversas),
    # path("mensagens/<str:numero>/", views.buscar_mensagens),
    # path("enviar/", views.enviar_mensagem),
    # path('bots/', views.lista_bots, name='lista_bots'),
    # path('bots/novo/', views.criar_bot, name='criar_bot'),
    # path('bots/<int:id>/editar/', views.editar_bot, name='editar_bot'),
    # path('bots/<int:id>/excluir/', views.excluir_bot, name='excluir_bot'),
]


