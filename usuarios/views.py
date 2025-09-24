# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncDate
import json
from django.contrib.auth import get_user_model, authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from pix.models import PixTransaction
from vendas.models import Venda
from django.utils import timezone
from datetime import datetime, time, timedelta
from .forms.UserCustom import LoginForm, RegisterForm  # forms personalizados
import csv
from django.http import HttpResponse
User = get_user_model()


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect("usuarios:dashboard")  # já logado

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate_mysql(username, password)  # função de autenticação custom no MySQL
        if user:
            # Pega o User customizado do banco
            django_user = User.objects.get(id=user['id'])
            django_login(request, django_user)  # registra sessão do Django
            messages.success(request, "Login realizado com sucesso!")
            return redirect("usuarios:dashboard")
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    form = LoginForm()
    return render(request, "usuarios/login.html", {"form": form})


# Logout
@login_required
def logout_view(request):
    django_logout(request)
    messages.success(request, "Você saiu com sucesso!")
    return redirect("usuarios:login")


# Cadastro
def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect("usuarios:dashboard")

    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # Cria usuário no banco
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # criptografa senha
            user.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect("usuarios:login")
        else:
            messages.error(request, "Erro ao criar conta. Verifique os dados.")

    return render(request, "usuarios/cadastro.html", {"form": form})


# Dashboard
@login_required
def dashboard_view(request):
    hoje = timezone.localdate()
    dias = [hoje - timedelta(days=i) for i in range(6, -1, -1)]

    entradas_diarias = []
    saidas_diarias = []

    for dia in dias:
        dia_inicio = datetime.combine(dia, time.min).replace(tzinfo=timezone.get_current_timezone())
        dia_fim = datetime.combine(dia, time.max).replace(tzinfo=timezone.get_current_timezone())

        entrada = PixTransaction.objects.filter(
            created_at__range=(dia_inicio, dia_fim)
        ).aggregate(total=Sum('valor'))['total'] or 0

        saida = Venda.objects.filter(
            data_venda__range=(dia_inicio, dia_fim)
        ).aggregate(total=Sum('valor'))['total'] or 0

        entradas_diarias.append(float(entrada))
        saidas_diarias.append(float(saida))

    total_entrada = sum(entradas_diarias)
    total_saida = sum(saidas_diarias)

    transacoes = [
        {'data': p.created_at, 'tipo': 'Entrada', 'valor': float(p.valor)}
        for p in PixTransaction.objects.all()
    ] + [
        {'data': v.data_venda, 'tipo': 'Saída', 'valor': float(v.valor)}
        for v in Venda.objects.all()
    ]
    transacoes = sorted(transacoes, key=lambda x: x['data'], reverse=True)

    transacoes_diarias = []
    for i, dia in enumerate(dias):
        crescimento = entradas_diarias[i] - saidas_diarias[i]
        transacoes_diarias.append({
            'data': dia.strftime('%d/%m'),
            'entrada': f"R$ {entradas_diarias[i]:.2f}".replace('.', ','),
            'saida': f"R$ {saidas_diarias[i]:.2f}".replace('.', ','),
            'crescimento': f"R$ {crescimento:.2f}".replace('.', ','),
        })

    crescimento_liquido = [e - s for e, s in zip(entradas_diarias, saidas_diarias)]

    context = {
        'labels_json': json.dumps([dia.strftime('%d/%m') for dia in dias]),
        'entradas_json': json.dumps(entradas_diarias),
        'saidas_json': json.dumps(saidas_diarias),
        'crescimento_json': json.dumps(crescimento_liquido),
        'total_entrada': total_entrada,
        'total_saida': total_saida,
        'transacoes': transacoes,
        'transacoes_diarias': transacoes_diarias,
        'request_user': request.user,
    }
    return render(request, "usuarios/dashboard.html", context)


# Função de autenticação custom (MySQL)
def authenticate_mysql(username, password):
    from django.db import connection
    from django.contrib.auth.hashers import check_password

    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, username, password FROM usuarios_user WHERE username = %s", [username]
    )
    row = cursor.fetchone()
    if row:
        user_id, db_username, db_password = row
        # Aqui você precisa validar a senha (hash ou plain)
        if db_password == password:
            return {'id': user_id, 'username': db_username}
    return None


@login_required
def exportar_transacoes_csv(request):
    # Cria a resposta HTTP com cabeçalho para download CSV
    response = HttpResponse(
        content_type='text/csv; charset=utf-8',
    )
    response['Content-Disposition'] = 'attachment; filename="transacoes.csv"'
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';')
    # Cabeçalho do CSV
    writer.writerow([
        'Data',
        'Entrada',
        'Saída',
        'Quem gerou o pagamento',
        'Para qual usuário foi',
        'Status',
        'Vencimento',
        'Produto',
        'Quantidade',
        'Valor do Produto',
        'Data de Venda',
        'Criado por'
    ])

    # PixTransactions
    for pix in PixTransaction.objects.all():
        writer.writerow([
            pix.created_at.strftime('%d/%m/%Y às %H:%M:%S'),
            float(pix.valor),  # Entrada
            0,  # Saída
            pix.user.username,
            pix.nome_pagador,
            pix.status,
            pix.vencimento.strftime('%d/%m/%Y') if pix.vencimento else '',
            '',  # Produto vazio
            '',  # Quantidade vazia
            '',  # Valor do produto vazio
            '',  # Data de venda vazia
            pix.user.username
        ])

    # Vendas
    for venda in Venda.objects.all():
        writer.writerow([
            venda.data_venda.strftime('%d/%m/%Y às %H:%M:%S'),
            0,  # Entrada
            float(venda.valor),  # Saída
            venda.criado_por.username,
            venda.cliente,
            'concluída',  # Status fixo (pode ajustar se quiser)
            '',  # Vencimento vazio
            venda.produto,
            venda.quantidade,
            float(venda.valor),
            venda.data_venda.strftime('%d/%m/%Y às %H:%M:%S'),
            venda.criado_por.username
        ])

    return response