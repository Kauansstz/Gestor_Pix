from .models import Configuracoes

def tema_e_notificacao_context(request):
    """
    Contexto global para templates:
    - tema: claro/escuro
    - notificacoes: True/False
    """
    try:
        config = Configuracoes.objects.get(id=1)
        return {
            "notificacoes": config.notificacoes
        }
    except Configuracoes.DoesNotExist:
        return {"notificacoes": True}  # fallback
