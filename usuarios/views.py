from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pix.models import PixTransaction
from vendas.models import Venda

from .forms.UserCustom import LoginForm, RegisterForm  # forms personalizados

# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect("usuarios:dashboard")  # já logado, vai direto pro dashboard

    form = LoginForm(request, data=request.POST or None)  # autenticação precisa passar request
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()  # AuthenticationForm fornece get_user()
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("usuarios:dashboard")
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, "usuarios/login.html", {"form": form})


# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu com sucesso!")
    return redirect("usuarios:login")


# Cadastro
def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect("usuarios:dashboard")

    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect("usuarios:login")
        else:
            messages.error(request, "Erro ao criar conta. Verifique os dados.")

    return render(request, "usuarios/cadastro.html", {"form": form})


# Dashboard
@login_required(login_url="usuarios:login")
def dashboard_view(request):
    return render(request, "usuarios/dashboard.html", {"user": request.user})

@login_required
def dashboard_view(request):
    # Calcular entrada e saída
    total_entrada = sum(p.valor for p in PixTransaction.objects.all())
    total_saida = sum(v.valor for v in Venda.objects.all())

    # Histórico de transações
    transacoes = []

    # Transações de Pix
    for p in PixTransaction.objects.all():
        transacoes.append({
            'data': p.created_at,  # <--- aqui
            'tipo': 'Entrada',
            'valor': p.valor
        })

    # Transações de Vendas
    for v in Venda.objects.all():
        transacoes.append({
            'data': v.data_venda,  # supondo que Venda tem campo 'data'
            'tipo': 'Saída',
            'valor': v.valor
        })

    # Ordena por data decrescente
    transacoes = sorted(transacoes, key=lambda x: x['data'], reverse=True)

    context = {
        'total_entrada': total_entrada,
        'total_saida': total_saida,
        'transacoes': transacoes,
    }
    return render(request, 'usuarios/dashboard.html', context)