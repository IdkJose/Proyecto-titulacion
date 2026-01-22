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

class UsuarioChangeForm(forms.ModelForm):
    is_active = forms.ChoiceField(
        choices=[(True, 'Activo'), (False, 'Inactivo')],
        label='Estado del Usuario',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'casa_departamento', 'telefono', 'rol', 'is_active')
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

from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ('titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'categoria', 'color')
        labels = {
            'titulo': 'Título del Evento',
            'descripcion': 'Descripción',
            'fecha_inicio': 'Fecha y Hora de Inicio',
            'fecha_fin': 'Fecha y Hora de Fin',
            'categoria': 'Categoría',
            'color': 'Color',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Reunión de la administración'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color', 'style': 'height: 40px; width: 100px;'}),
        }

