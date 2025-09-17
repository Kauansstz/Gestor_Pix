# relatorios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Relatorio
from .forms.RelatorioCustom import RelatorioForm
import csv
from django.http import HttpResponse

@login_required
def listar_relatorios(request):
    relatorios = Relatorio.objects.all()
    return render(request, 'relatorios/listar_relatorios.html', {'relatorios': relatorios})

@login_required
def criar_relatorio(request):
    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if form.is_valid():
            relatorio = form.save(commit=False)
            relatorio.criado_por = request.user
            relatorio.save()
            messages.success(request, 'Relatório criado com sucesso!')
            return redirect('relatorios:listar_relatorios')
        else:
            messages.error(request, 'Erro ao criar relatório.')
    else:
        form = RelatorioForm()
    return render(request, 'relatorios/criar_relatorio.html', {'form': form})

@login_required
def exportar_csv(request):
    relatorios = Relatorio.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorios.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Título', 'Descrição', 'Data', 'Criado Por', 'Atualizado Em'])
    for r in relatorios:
        writer.writerow([r.id, r.titulo, r.descricao, r.data, r.criado_por.username, r.atualizado_em])
    return response


@login_required
def relatorio_detail(request, pk):
    try:
        relatorio = Relatorio.objects.get(pk=pk)
    except Relatorio.DoesNotExist:
        messages.error(request, 'Relatório não encontrado.')
        return redirect('relatorios:listar_relatorios')
    
    return render(request, 'relatorios/relatorio_detail.html', {'relatorio': relatorio})