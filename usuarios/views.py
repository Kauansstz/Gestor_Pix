from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
import hashlib
from pix.models import PixTransaction
from vendas.models import Venda
from .utils.LoginRequired import authenticate_mysql, login_required_session
from .utils.LoginRequired import SessionUser
# Classe para simular request.user com sessão


# Login
def login_view(request):
    if request.session.get('user_id'):
        return redirect("usuarios:dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate_mysql(username, password)
        if user:
            # Cria sessão
            request.user = SessionUser(user['id'], user['username'])
            # Simula request.user
            request.session['user_id'] = user['id']
            request.session['username'] = user['username']
            messages.success(request, "Login realizado com sucesso!")
            request.user = SessionUser(user['id'], user['username'])
            return render(request,"usuarios/dashboard.html")
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, "usuarios/login.html")

# Logout
def logout_view(request):
    request.session.flush()
    messages.success(request, "Você saiu com sucesso!")
    return redirect("usuarios:login")

# Cadastro
def cadastro_view(request):
    if request.session.get('user_id'):
        return redirect("usuarios:dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            messages.error(request, "Todos os campos são obrigatórios.")
            return render(request, "usuarios/cadastro.html")

        hashed = hashlib.sha256(password.encode()).hexdigest()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios_user (username, password, email, is_active, date_joined) "
                    "VALUES (%s, %s, %s, %s, NOW())",
                    [username, hashed, email, 1]
                )
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect("usuarios:login")
        except Exception as e:
            messages.error(request, f"Erro ao criar conta: {str(e)}")

    return render(request, "usuarios/cadastro.html")

# Dashboard


@login_required_session
def dashboard_view(request):
    # Se estiver usando nossa sessão manual, simula request.user
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        if request.session.get('user_id'):
            request.user = SessionUser(request.session['user_id'], request.session['username'])
        else:
            return redirect("usuarios:login")

    total_entrada = sum(p.valor for p in PixTransaction.objects.all())
    total_saida = sum(v.valor for v in Venda.objects.all())

    transacoes = []

    for p in PixTransaction.objects.all():
        transacoes.append({
            'data': p.created_at,
            'tipo': 'Entrada',
            'valor': p.valor
        })

    for v in Venda.objects.all():
        transacoes.append({
            'data': v.data_venda,
            'tipo': 'Saída',
            'valor': v.valor
        })

    transacoes = sorted(transacoes, key=lambda x: x['data'], reverse=True)

    context = {
        'total_entrada': total_entrada,
        'total_saida': total_saida,
        'transacoes': transacoes,
        'user': request.user
    }
    return render(request, 'usuarios/dashboard.html', context)
