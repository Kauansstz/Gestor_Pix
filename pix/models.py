from django.db import models
from django.conf import settings

class PixTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_pagador = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    vencimento = models.DateField(blank=True, null=True)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    data_pagamento = models.DateTimeField(null=True, blank=True)
    link_pix = models.URLField(blank=True, null=True)
    pago = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="pendente")
    def __str__(self):
            return f"Pix {self.id} - {self.valor} - Pago: {self.pago}"