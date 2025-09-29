from django import forms
from relatorios.models import Relatorio

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['titulo', 'descricao', 'data']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500',
                'placeholder': 'Título'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500',
                'placeholder': 'Descrição',
                'rows': 4
            }),
            'data': forms.DateInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500',
                'type': 'date'
            }),
        }
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'data': 'Data',
        }
