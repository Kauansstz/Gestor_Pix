from django.db import models
from django.conf import settings

class Venda(models.Model):
    cliente = models.CharField(max_length=150)
    produto = models.CharField(max_length=150)
    quantidade = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cliente} - {self.produto}'

    class Meta:
        ordering = ['-data_venda']  # ordena pela data mais recente
