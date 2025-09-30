from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Configuracoes
from .forms.ConfiguracoesForm import ConfiguracoesForm

def configuracoes_view(request):
    # garante que sempre exista 1 configuração
    config, created = Configuracoes.objects.get_or_create(id=1)

    if request.method == "POST":
        form = ConfiguracoesForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Configurações salvas com sucesso!")
            return redirect("config:configuracoes")  # nome da rota
        else:
            messages.error(request, "Erro ao salvar as configurações.")
    else:
        form = ConfiguracoesForm(instance=config)

    return render(request, "configuracoes/config.html", {"form": form})
