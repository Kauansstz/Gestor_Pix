from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Venda
from .forms.VendasCustom import VendaForm

@login_required
def listar_vendas(request):
    vendas = Venda.objects.all()
    return render(request, 'vendas/listar_vendas.html', {'vendas': vendas})

@login_required
def nova_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.criado_por = request.user
            venda.save()
            messages.success(request, 'Venda cadastrada com sucesso!')
            return redirect('vendas:listar_vendas')
    else:
        form = VendaForm()
    return render(request, 'vendas/nova_venda.html', {'form': form})
