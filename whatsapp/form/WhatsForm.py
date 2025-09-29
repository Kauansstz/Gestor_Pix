from django import forms
from whatsapp.models import WhatsCustom

class WhatsCustomForm(forms.ModelForm):
    class Meta:
        model = WhatsCustom
        fields = ['nome_cliente', 'numero_cliente', 'tipo_midia', 'msg_text', 'cover', 'link_pix',"email", "status_cliente", "observacao", "file"]
        widgets = {
            'nome_cliente': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md'}),
            'numero_cliente': forms.TextInput(attrs={'type': 'tel', 'pattern': '[0-9]+', 'class': 'w-full p-3 border border-gray-300 rounded-md'}),
            'email': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md'}),
            'tipo_midia': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md', 'id': 'tipo_midia'}),
            'status_cliente': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md', 'id': 'status_cliente'}),
            'observacao': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md', 'rows': 4, 'maxlength': '1000', 'id': 'campo_texto'}),
            'msg_text': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md', 'rows': 4, 'maxlength': '1000', 'id': 'campo_texto'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md', 'id': 'campo_cover'}),
            'file': forms.ClearableFileInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md', 'id': 'campo_file'}),
            'link_pix': forms.URLInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md', 'id': 'campo_link'}),
        }
        labels = {
            "nome_cliente": "Nome do Cliente",
            "numero_cliente": "Número do Cliente",
            "tipo_midia": "Tipo de Mídia",
            "msg_text": "Mensagem de Texto",
            "cover": "Arquivo",
            "link_pix": "Links",
            "email": "E-mail",
            "status_cliente": "Status do Cliente",
            "observacao": "Observação",
            "file": "Arquivo (Excel ou CSV)"
        }
