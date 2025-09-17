from django import forms
from vendas.models import Venda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'produto', 'quantidade', 'valor']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nome do cliente'}),
            'produto': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Produto'}),
            'quantidade': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Quantidade'}),
            'valor': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Valor'}),
        }
