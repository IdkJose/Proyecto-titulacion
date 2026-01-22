from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'casa_departamento', 'telefono', 'rol')
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'casa_departamento': 'Casa o Departamento',
            'telefono': 'Teléfono',
            'rol': 'Rol de usuario',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: juanperez'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'juan@ejemplo.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pérez'}),
            'casa_departamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Casa 15'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0991234567'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }
