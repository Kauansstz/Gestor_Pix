import requests
import qrcode
from io import BytesIO
import base64
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import PixTransaction
from .forms.PixForm import PixForm
from usuarios.utils.LoginRequired import login_required_session

# Token da sua loja no PicPay (fixo, não dinâmico!)
CLIENT_ID = "0bdba77d-75b2-4bf9-bbfb-db6c59f5bfa1"
CLIENT_SECRET = "A6YbbuXgRU4GIkGxCwpLb2g7x1965iUh"

def gerar_token_picpay():
    url = "https://checkout-api.picpay.com/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("access_token")  # ESTE é o token válido
    except Exception as e:
        print("Erro ao gerar token:", e)
        return None


# Função para criar cobrança no PicPay
def criar_cobranca_picpay(valor, referencia, callback_url):
    token = gerar_token_picpay()
    if not token:
        return {"error": "Não foi possível gerar token PicPay"}

    url = "https://appws.picpay.com/ecommerce/public/payments"
    payload = payload = {
    "referenceId": str(referencia),
    "callbackUrl": callback_url,
    "returnUrl": "https://localhost/pagamento-sucesso",
    "value": float(valor),
    "buyer": {
        "firstName": "Kauan",
        "lastName": "Dos Santos de Souza",
        "document": "13858197904",
        "email": "kauansantosdesouza45@gmail.com",
        "phone": "+5548998345181"
    }}  # seu payload do comprador
    headers = {
        "Content-Type": "application/json",
        "x-picpay-token": token
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Erro ao criar cobrança:", e, response.text if 'response' in locals() else "")
        return {"error": "Falha ao criar cobrança"}


# Função para gerar QR Code em base64
def gerar_qrcode_base64(url):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Listar Pix
@login_required_session
def listar_pix(request):
    pix_list = PixTransaction.objects.all()
    return render(request, 'pix/listar_pix.html', {'pix_list': pix_list})

# Gerar Pix
@login_required_session
def gerar_pix(request):
    if request.method == 'POST':
        form = PixForm(request.POST)
        if form.is_valid():
            pix = form.save(commit=False)
            pix.user = request.user
            pix.save()

            callback_url = request.build_absolute_uri('/pix/webhook_picpay/')
            cobranca = criar_cobranca_picpay(pix.valor, pix.id, callback_url)

            if cobranca.get("error"):
                messages.error(request, cobranca["error"])
                return redirect('pix:gerar_pix')

            pix.link_pix = cobranca.get("paymentUrl")
            pix.save()

            qr_base64 = gerar_qrcode_base64(pix.link_pix)
            return render(request, 'pix/gerar_pix_sucesso.html', {'pix': pix, 'qr_base64': qr_base64})
        else:
            messages.error(request, 'Erro ao gerar Pix.')
    else:
        form = PixForm()
    return render(request, 'pix/gerar_pix_sucesso.html', {'form': form})

# Webhook PicPay
@csrf_exempt
def webhook_picpay(request):
    if request.method == "POST":
        data = json.loads(request.body)
        reference_id = data.get("referenceId")
        status = data.get("status")  # paid, cancelled, failed

        try:
            pix = PixTransaction.objects.get(id=reference_id)
            if status == "paid" and not pix.pago:
                pix.pago = True
                pix.data_pagamento = timezone.now()
                pix.save()
                print(f"Cobrança {reference_id} foi paga!")
        except PixTransaction.DoesNotExist:
            print(f"Pix {reference_id} não encontrado")

    return JsonResponse({"status": "ok"})
