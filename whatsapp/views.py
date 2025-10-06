from django.http import HttpResponse
from whatsapp.form.WhatsForm import WhatsCustomForm
from .models import WhatsCustom
from django.shortcuts import get_object_or_404, redirect, render
from usuarios.utils.LoginRequired import login_required_session
from django.contrib import messages
import pandas as pd
import csv


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


def import_client(request):
    if request.method == 'POST':
        form = WhatsCustomForm(request.POST, request.FILES)
        if form.is_valid():  
            arquivo = request.FILES["file"]
            try:
                if arquivo.name.endswith(".csv"):
                    df = pd.read_csv(arquivo)
                else:
                    df = pd.read_excel(arquivo)
                
                importados = 0
                ignorados = 0
                
                for _, row in df.iterrows():
                    numero = str(row.get("numero_cliente", "")).strip()
                    
                    if not numero:
                        ignorados += 1
                        continue
                    
                    if WhatsCustom.objects.filter(numero_cliente=numero).exists():
                        ignorados += 1
                        continue
                        
                    WhatsCustom.objects.create(
                        nome_cliente=row.get("nome_cliente", ""),
                        numero_cliente=numero,
                        email=row.get("email", ""),
                        status_cliente=row.get("status_cliente", "Ativo"),
                        observacao=row.get("observacao", "")
                    )
                    importados += 1
                    
                messages.success(request, f"{importados} clientes importados, {ignorados} ignorados.")
                return redirect("whats:importar_clientes")
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")
    else:
        form = WhatsCustomForm()

    return render(request, "whatsapp/client/import.html", {"form": form})


# Quando api estiver disponivel
# from django.shortcuts import render
# from django.http import JsonResponse
# import requests

# WHATSAPP_TOKEN = "SEU_TOKEN_DO_META"
# WHATSAPP_PHONE_ID = "SEU_PHONE_ID"  # vem do Meta App

# def chat_view(request):
#     """Renderiza o chat com histórico básico."""
#     return render(request, "chat.html")

# def listar_conversas(request):
#     """Simula listagem de conversas (você pode integrar com seu banco)."""
#     conversas = [
#         {"nome": "João", "numero": "5511999999999", "ultima_msg": "Olá, tudo bem?"},
#         {"nome": "Maria", "numero": "5511988888888", "ultima_msg": "Pedido enviado ✅"},
#     ]
#     return JsonResponse(conversas, safe=False)

# def buscar_mensagens(request, numero):
#     """Chama a API do WhatsApp (ou seu DB) para buscar mensagens do cliente."""
#     # Exemplo fictício — você pode trocar por requisição real:
#     mensagens = [
#         {"texto": "Oi, tudo bem?", "tipo": "recebida"},
#         {"texto": "Tudo ótimo, e você?", "tipo": "enviada"},
#     ]
#     return JsonResponse({"mensagens": mensagens})

# def enviar_mensagem(request):
#     """Envia mensagem de texto para o WhatsApp."""
#     numero = request.POST.get("numero")
#     texto = request.POST.get("mensagem")

#     url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
#     headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
#     data = {
#         "messaging_product": "whatsapp",
#         "to": numero,
#         "type": "text",
#         "text": {"body": texto}
#     }

#     response = requests.post(url, headers=headers, json=data)
#     return JsonResponse(response.json())


#bots!!!!!!!
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Bot

# def lista_bots(request):
#     bots = Bot.objects.all()
#     return render(request, 'bots.html', {'bots': bots})

# def criar_bot(request):
#     if request.method == 'POST':
#         Bot.objects.create(
#             nome=request.POST['nome'],
#             numero=request.POST['numero'],
#             mensagem_auto=request.POST['mensagem_auto'],
#             ativo='ativo' in request.POST
#         )
#         return redirect('lista_bots')
#     return render(request, 'editar_bot.html', {'bot': None})

# def editar_bot(request, id):
#     bot = get_object_or_404(Bot, id=id)
#     if request.method == 'POST':
#         bot.nome = request.POST['nome']
#         bot.numero = request.POST['numero']
#         bot.mensagem_auto = request.POST['mensagem_auto']
#         bot.ativo = 'ativo' in request.POST
#         bot.save()
#         return redirect('lista_bots')
#     return render(request, 'editar_bot.html', {'bot': bot})

# def excluir_bot(request, id):
#     bot = get_object_or_404(Bot, id=id)
#     bot.delete()
#     return redirect('lista_bots')


# Disparo de mensagens
# from django.shortcuts import render, redirect
# from .models import Contato, Agendamento
# from django.utils import timezone

# def listar_agendamentos(request):
#     agendamentos = Agendamento.objects.all().order_by('data_envio')
#     return render(request, 'agendamentos.html', {'agendamentos': agendamentos})

# def criar_agendamento(request):
#     if request.method == 'POST':
#         contato_id = request.POST['contato']
#         mensagem = request.POST['mensagem']
#         data_envio = request.POST['data_envio']

#         contato = Contato.objects.get(id=contato_id)
#         Agendamento.objects.create(
#             contato=contato,
#             mensagem_template=mensagem,
#             data_envio=data_envio
#         )
#         return redirect('listar_agendamentos')

#     contatos = Contato.objects.all()
#     return render(request, 'criar_agendamento.html', {'contatos': contatos})
