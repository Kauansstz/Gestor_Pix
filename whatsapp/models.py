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
    file = models.FileField(label="Selecione o arquivo (Excel ou CSV)" , upload_to="static/file/%Y/%m/%d/", blank=True, default="")
    msg_text = models.CharField(max_length=1000,default="", blank=True)
    email = models.CharField(blank=True, max_length=255)
    status_cliente = models.CharField(max_length=255, blank=True, choices=STATUS_CLIENTE)
    observacao= models.CharField(max_length=1000, blank=True, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,  choices=STATUS_MSG, default="PENDING")
    erro = models.TextField(blank=True, null=True)