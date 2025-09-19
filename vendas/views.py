# vendas/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Venda
from .forms.VendasCustom import VendaForm
from usuarios.utils.LoginRequired import login_required_session




@login_required_session
def listar_vendas(request):
    vendas = Venda.objects.all()
    return render(request, 'vendas/listar_vendas.html', {'vendas': vendas})

@login_required_session
def nova_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.criado_por = request.user  # usa SessionUser
            venda.save()
            messages.success(request, 'Venda cadastrada com sucesso!')
            return redirect('vendas:listar_vendas')
        else:
            messages.error(request, 'Erro ao cadastrar a venda.')
    else:
        form = VendaForm()
    return render(request, 'vendas/nova_venda.html', {'form': form})
