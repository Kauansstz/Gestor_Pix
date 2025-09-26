from django.shortcuts import render
from whatsapp.form.WhatsForm import WhatsCustomForm
from django.contrib import messages
from usuarios.utils.LoginRequired import login_required_session

@login_required_session
def message(request):
    if request.method == 'POST':
        form = WhatsCustomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso!')
        else:
            messages.error(request, 'Erro ao cadastrar a venda.')
    else:
        form = WhatsCustomForm()

    return render(request, 'whatsapp/message.html', {'form': form})