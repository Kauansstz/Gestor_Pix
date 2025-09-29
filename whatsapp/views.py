import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from whatsapp.form.WhatsForm import WhatsCustomForm
from django.contrib import messages
from usuarios.utils.LoginRequired import login_required_session
from .models import WhatsCustom

@login_required_session
def message(request):
    if request.method == 'POST':
        form = WhatsCustomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso!')
        else:
            messages.error(request, 'Erro ao cadastrar a venda.')
    else:
        form = WhatsCustomForm()

    return render(request, 'whatsapp/message.html', {'form': form})

@login_required_session
def relatorio_whats(request):
    form = WhatsCustom.objects.all()
    return render(request, 'whatsapp/relatorio_whats.html', {"relatorios": form})

@login_required_session
def list_client(request):
    form = WhatsCustom.objects.all()
    return render(request, 'whatsapp/client/list_client.html', {"list": form})

@login_required_session
def exportar_csv_relatorio(request):
    relatorios = WhatsCustom.objects.all()
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="relatorios.csv"'
    response.write('\ufeff'.encode('utf8'))  # BOM para Excel
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome do Cliente', 'Número', 'Tipo de Midía', 'Status', 'Data de Envio'])

    for r in relatorios:
        writer.writerow([
            r.id,
            r.nome_cliente,
            r.numero_cliente,
            r.tipo_midia,
            r.status,  # agora seguro porque é User custom
            r.data_envio.strftime('%d-%m-%y %H:%M')
        ])
    return response
@login_required_session
def exportar_csv_list_client(request):
    lista = WhatsCustom.objects.all()
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="relatorios.csv"'
    response.write('\ufeff'.encode('utf8'))  # BOM para Excel
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Nome do Cliente', 'Número', 'Tipo de Midía', 'Status', 'Data de Envio'])

    for l in lista:
        writer.writerow([
            l.id,
            l.nome_cliente,
            l.numero_cliente,
            l.tipo_midia,
            l.status,  # agora seguro porque é User custom
            l.data_envio.strftime('%d-%m-%y %H:%M')
        ])
    return response

@login_required_session
def editar_relatorio(request, pk):
    relatorio = get_object_or_404(WhatsCustomForm, pk=pk)

    if request.method == 'POST':
        form = WhatsCustomForm(request.POST, instance=relatorio)
        if form.is_valid():
            form.save()  # automaticamente atualiza 'atualizado_em'
            messages.success(request, 'Relatório atualizado com sucesso!')
            return redirect('relatorios:listar_relatorios')
        else:
            messages.error(request, 'Erro ao atualizar o relatório.')
    else:
        form = WhatsCustomForm(instance=relatorio)

    return render(request, 'whatsapp/editar_relatorio.html', {'form': form, 'relatorio': relatorio})

@login_required_session
def new_client(request):
    if request.method == 'POST':
        form = WhatsCustomForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Cliente cadastrado!')
            return redirect('whats:new_client')
        else:
            messages.error(request, "Erro ao cadastrar o cliente")
    else:
        form = WhatsCustomForm()
    return render(request, "whatsapp/client/new_client.html", {"client": form, })