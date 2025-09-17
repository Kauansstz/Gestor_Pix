from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PixTransaction
from .forms.PixForm import PixForm

@login_required
def listar_pix(request):
    pix_list = PixTransaction.objects.all()
    return render(request, 'pix/listar_pix.html', {'pix_list': pix_list})

@login_required
def gerar_pix(request):
    if request.method == 'POST':
        form = PixForm(request.POST)
        if form.is_valid():
            pix = form.save(commit=False)  
            pix.user = request.user  
            form.save()
            messages.success(request, 'Pix gerado com sucesso!')
            return redirect('pix:listar_pix')
        else:
            messages.error(request, 'Erro ao gerar Pix.')
    else:
        form = PixForm()
    return render(request, 'pix/gerar_pix.html', {'form': form})
