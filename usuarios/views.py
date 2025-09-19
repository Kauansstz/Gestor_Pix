# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from pix.models import PixTransaction
from vendas.models import Venda

from .forms.UserCustom import LoginForm, RegisterForm  # forms personalizados

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
    # Calcula entradas e saídas
    total_entrada = sum(p.valor for p in PixTransaction.objects.all())
    total_saida = sum(v.valor for v in Venda.objects.all())

    # Histórico de transações
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

    # Ordena por data decrescente
    transacoes = sorted(transacoes, key=lambda x: x['data'], reverse=True)

    context = {
        'total_entrada': total_entrada,
        'total_saida': total_saida,
        'transacoes': transacoes,
        'request_user': request.user,  # para templates
    }
    return render(request, "usuarios/dashboard.html", context)


# Função de autenticação custom (MySQL)
def authenticate_mysql(username, password):
    """
    Exemplo de autenticação manual no MySQL.
    Retorna dict com 'id' e 'username' se válido, senão None
    """
    from django.db import connection
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
