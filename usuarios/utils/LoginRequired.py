from django.shortcuts import redirect
from django.db import connection

class SessionUser:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.is_authenticated = True

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
        if not request.session.get('user_id'):
            return redirect('usuarios:login')
        # Simula request.user
        request.user = SessionUser('user_id','username')
        return view_func(request, *args, **kwargs)
    return wrapper