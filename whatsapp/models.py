from django.db import models
from django.core.validators import RegexValidator

class WhatsCustom(models.Model):
    TIPO_MIDIA =[
        
        ("TEXT", "Texto"),
        ("IMAGEM", "Imagem"),
        ]
    STATUS_MSG =[
        ("PENDING", "Pendente"),
        ("SENT", "Enviada"),
        ("DELIVERED", "Entregue"),
        ("READ", "Lida"),
        ("ERROR", "Erro"),
    ]
    STATUS_CLIENTE =[
        
        ("ATIVO", "Ativo"),
        ("INATIVO", "Inativo"),     
    ]
    numero_valido = RegexValidator(
        regex=r'^\d+$',
        message="O número deve conter apenas dígitos."
    )
    mensagem_id = models.CharField(max_length=100, blank=True, null=True)
    nome_cliente = models.CharField(max_length=100)
    numero_cliente = models.CharField(
        max_length=15,
        validators=[numero_valido],
        help_text="Digite apenas números"
    )
    tipo_midia = models.CharField(max_length=20, choices=TIPO_MIDIA, default="--------")
    link_pix = models.URLField()
    cover = models.ImageField(upload_to="static/covers/%Y/%m/%d/", blank=True, default="")
    file = models.FileField(upload_to="static/file/%Y/%m/%d/", blank=True, default="")
    msg_text = models.CharField(max_length=1000,default="", blank=True)
    email = models.CharField(blank=True, max_length=255)
    status_cliente = models.CharField(max_length=255, blank=True, choices=STATUS_CLIENTE)
    observacao= models.CharField(max_length=1000, blank=True, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,  choices=STATUS_MSG, default="PENDING")
    erro = models.TextField(blank=True, null=True)
    
# Bots
# class Bot(models.Model):
#     nome = models.CharField(max_length=100)
#     numero = models.CharField(max_length=20)
#     mensagem_auto = models.TextField(blank=True)
#     ativo = models.BooleanField(default=True)

#     def __str__(self):
#         return self.nome

# Disparo de mensagens
# class Contato(models.Model):
#     nome = models.CharField(max_length=100)
#     numero = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.nome} ({self.numero})"

# class Agendamento(models.Model):
#     contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
#     mensagem_template = models.TextField()
#     data_envio = models.DateTimeField()
#     enviado = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Agendamento para {self.contato.nome} em {self.data_envio}"


# CRM 
# from django.db import models

# # Contato / Lead
# class Cliente(models.Model):
#     STATUS_CHOICES = [
#         ('LEAD', 'Lead'),
#         ('CONTATO', 'Contato'),
#         ('PROPOSTA', 'Proposta'),
#         ('FECHADO', 'Fechado'),
#     ]
#     nome = models.CharField(max_length=100)
#     telefone = models.CharField(max_length=20)
#     email = models.EmailField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='LEAD')
#     data_criacao = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.nome

# # Histórico de mensagens
# class Mensagem(models.Model):
#     TIPO_CHOICES = [
#         ('ENVIADO', 'Enviado'),
#         ('RECEBIDO', 'Recebido'),
#         ('TEMPLATE', 'Template'),
#     ]
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mensagens')
#     texto = models.TextField()
#     tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
#     status = models.CharField(max_length=50, blank=True)  # enviado, entregue, lida
#     data_envio = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.tipo} - {self.cliente.nome}"

# Relatórios e Métricas
# from django.db import models

# class Cliente(models.Model):
#     STATUS_CHOICES = [
#         ('LEAD', 'Lead'),
#         ('CONTATO', 'Contato'),
#         ('PROPOSTA', 'Proposta'),
#         ('FECHADO', 'Fechado'),
#     ]
#     nome = models.CharField(max_length=100)
#     telefone = models.CharField(max_length=20)
#     email = models.EmailField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='LEAD')
#     data_criacao = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.nome

# class Mensagem(models.Model):
#     TIPO_CHOICES = [
#         ('ENVIADO', 'Enviado'),
#         ('RECEBIDO', 'Recebido'),
#         ('TEMPLATE', 'Template'),
#     ]
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mensagens')
#     texto = models.TextField()
#     tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
#     status = models.CharField(max_length=50, blank=True)  # enviado, entregue, lido
#     data_envio = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.tipo} - {self.cliente.nome}"
