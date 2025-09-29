from django import forms
from pix.models import PixTransaction

class PixForm(forms.ModelForm):
    class Meta:
        model = PixTransaction
        fields = ['nome_pagador', 'valor', 'descricao', 'vencimento']
        widgets = {
            'nome_pagador': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md',
                'placeholder': 'Nome do pagador'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md',
                'placeholder': 'Valor'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md',
                'placeholder': 'Descrição'
            }),
            'vencimento': forms.DateInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md',
                'type': 'date'
            }),
        }
        labels = {
            'nome_pagador': 'Nome do Pagador',
            'valor': 'Valor',
            'descricao': 'Descrição',
            'vencimento': 'Vencimento',
        }
