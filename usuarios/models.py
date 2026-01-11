from django.db import models
from django.contrib.auth.models import AbstractUser
# Modelo de Usuario Personalizado para el Conjunto Selva Alegre
class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    Agrega campos específicos para vecinos del conjunto habitacional.
    """
    
    # Choices para el campo rol
    ROLES = [
        ('admin', 'Administrador'),
        ('vecino', 'Vecino'),
    ]
    
    # Campos adicionales
    telefono = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text='Número de teléfono del usuario'
    )
    
    casa_departamento = models.CharField(
        max_length=14,
        blank=False,
        null=False,
        help_text='Número de casa o departamento (ej: Casa 15, Depto 3B)'
    )
    
    rol = models.CharField(
        max_length=10,
        choices=ROLES,
        default='vecino',
        help_text='Rol del usuario en el sistema'
    )
    
    foto_perfil = models.ImageField(
        upload_to='usuarios/fotos_perfil/',
        blank=True,
        null=True,
        help_text='Foto de perfil del usuario'
    )
    
    activo = models.BooleanField(
        default=True,
        help_text='Indica si el usuario está activo en el conjunto'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de registro en el sistema'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['casa_departamento', 'last_name']
    
    def __str__(self):
        """Representación en string del usuario"""
        if self.casa_departamento:
            return f"{self.get_full_name()} - {self.casa_departamento}"
        return self.get_full_name() or self.username
    
    def es_administrador(self):
        """Método helper para verificar si el usuario es administrador"""
        return self.rol == 'admin'