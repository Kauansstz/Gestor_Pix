from django.db import models

class Configuracoes(models.Model):
    # PIX
    chave_pix = models.CharField(max_length=255, blank=True, null=True)
    banco = models.CharField(max_length=100, blank=True, null=True)

    # WhatsApp
    numero_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    mensagem_padrao = models.TextField(blank=True, null=True)
    enviar_automatico = models.BooleanField(default=False)

    # Preferências
    notificacoes = models.BooleanField(default=True)

    def __str__(self):
        return "Configurações do Sistema"
