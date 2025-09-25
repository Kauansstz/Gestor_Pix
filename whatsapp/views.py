from django.shortcuts import render

def message(request):
    return render(request, "whatsapp/message.html")
