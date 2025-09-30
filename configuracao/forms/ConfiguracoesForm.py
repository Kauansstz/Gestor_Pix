from django import forms
from configuracao.models import Configuracoes

class ConfiguracoesForm(forms.ModelForm):
    class Meta:
        model = Configuracoes
        fields = [
            "chave_pix", "banco",
            "numero_whatsapp", "mensagem_padrao", "enviar_automatico",
            "notificacoes"
        ]
        widgets = {
            "chave_pix": forms.TextInput(attrs={"class": "w-full border px-3 py-2 rounded"}),
            "banco": forms.TextInput(attrs={"class": "w-full border px-3 py-2 rounded"}),
            "numero_whatsapp": forms.TextInput(attrs={"class": "w-full border px-3 py-2 rounded"}),
            "mensagem_padrao": forms.Textarea(attrs={"class": "w-full border px-3 py-2 rounded h-24"}),
            
        }
