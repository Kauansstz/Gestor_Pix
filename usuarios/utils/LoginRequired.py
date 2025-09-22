from django.shortcuts import redirect
from django.db import connection

# Função para autenticar usuário via MySQL
def authenticate_mysql(username, password):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, username FROM usuarios_user WHERE username=%s AND password=%s AND is_active=1",
            [username, password]
        )
        user = cursor.fetchone()
        if user:
            return {"id": user[0], "username": user[1]}
    return None

def login_required_session(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('usuarios:login')
        # Simula request.user
        return view_func(request, *args, **kwargs)
    return wrapper