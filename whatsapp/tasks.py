from celery import shared_task
import requests
from .models import Agendamento
from django.utils import timezone

WHATSAPP_TOKEN = "SEU_TOKEN_DA_META"
WHATSAPP_PHONE_ID = "SEU_PHONE_ID"

@shared_task
def processar_agendamentos():
    agendamentos = Agendamento.objects.filter(enviado=False, data_envio__lte=timezone.now())
    for ag in agendamentos:
        # Disparo via API do WhatsApp
        url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        payload = {
            "messaging_product": "whatsapp",
            "to": ag.contato.numero,
            "type": "template",
            "template": {
                "name": "nome_do_template_aprovado",
                "language": {"code": "pt_BR"},
                "components": [{"type": "body", "parameters":[{"type":"text", "text": ag.mensagem_template}]}]
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            ag.enviado = True
            ag.save()
