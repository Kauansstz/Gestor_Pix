from django import forms
from vendas.models import Venda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'produto', 'quantidade', 'valor']
        widgets = {
            'cliente': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md',
                'placeholder': 'Nome do cliente'
            }),
            'produto': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md',
                'placeholder': 'Produto'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md',
                'placeholder': 'Quantidade'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md',
                'placeholder': 'Valor'
            }),
        }
        labels = {
            'cliente': 'Cliente',
            'produto': 'Produto',
            'quantidade': 'Quantidade',
            'valor': 'Valor',
        }
