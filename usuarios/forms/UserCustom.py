from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Form de Login
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded p-2 mb-3 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Usuário'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded p-2 mb-3 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Senha'
        })
    )

# Form de Cadastro
class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded p-2 mb-3 focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Usuário'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded p-2 mb-3 focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Senha'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded p-2 mb-3 focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Confirme a senha'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
