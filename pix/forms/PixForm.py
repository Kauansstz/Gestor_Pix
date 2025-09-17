from django import forms
from pix.models import PixTransaction

class PixForm(forms.ModelForm):
    class Meta:
        model = PixTransaction
        fields = ['nome_pagador', 'valor', 'descricao', 'vencimento']
        widgets = {
            'nome_pagador': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nome do pagador'}),
            'valor': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Valor'}),
            'descricao': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Descrição'}),
            'vencimento': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
        }
