from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Administrador"),
        ("vendedor", "Vendedor"),
        ("cliente", "Cliente"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="cliente")
    
    # Evita conflito de grupos e permissões
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_user_set',  # nome exclusivo
        blank=True,
        help_text='Grupos do usuário.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_user_permissions_set',  # nome exclusivo
        blank=True,
        help_text='Permissões do usuário.',
        verbose_name='user permissions',
    )
