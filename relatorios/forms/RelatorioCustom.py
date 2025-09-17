from django import forms
from relatorios.models import Relatorio

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['titulo', 'descricao', 'data']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Título'}),
            'descricao': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Descrição', 'rows': 4}),
            'data': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
        }
