# pix/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PixTransaction
from .forms.PixForm import PixForm
from usuarios.utils.LoginRequired import login_required_session

# Classe para simular request.user a partir da sessão


@login_required_session
def listar_pix(request):
    pix_list = PixTransaction.objects.all()
    return render(request, 'pix/listar_pix.html', {'pix_list': pix_list})

@login_required_session
def gerar_pix(request):
    if request.method == 'POST':
        form = PixForm(request.POST)
        if form.is_valid():
            pix = form.save(commit=False)
            pix.user = request.user  # usa SessionUser
            pix.save()
            messages.success(request, 'Pix gerado com sucesso!')
            return redirect('pix:listar_pix')
        else:
            messages.error(request, 'Erro ao gerar Pix.')
    else:
        form = PixForm()
    return render(request, 'pix/gerar_pix.html', {'form': form})
