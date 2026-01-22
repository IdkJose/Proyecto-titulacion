from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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
    email = models.EmailField(
        unique=True,
        blank=True,
        help_text='Correo electrónico del usuario'
    )

    first_name = models.CharField(
        max_length=150,
        blank=False,
        help_text='Nombre del usuario'
    )

    last_name = models.CharField(
        max_length=150,
        blank=False,
        help_text='Apellido del usuario'
    )

    telefono = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='El teléfono solo puede contener números'
            )
        ],
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


class Evento(models.Model):
    """
    Modelo para guardar eventos del calendario.
    Cada evento pertenece a un usuario específico.
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='eventos',
        help_text='Usuario propietario del evento'
    )
    
    titulo = models.CharField(
        max_length=200,
        help_text='Título del evento'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text='Descripción detallada del evento'
    )
    
    fecha_inicio = models.DateTimeField(
        help_text='Fecha y hora de inicio del evento'
    )
    
    fecha_fin = models.DateTimeField(
        help_text='Fecha y hora de fin del evento'
    )
    
    # Choices para categorías de eventos
    CATEGORIAS = [
        ('minga', 'Minga'),
        ('reunion', 'Reunión'),
        ('mantenimiento', 'Mantenimiento'),
        ('evento_social', 'Evento Social'),
        ('otro', 'Otro'),
    ]
    
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default='otro',
        help_text='Categoría del evento'
    )
    
    color = models.CharField(
        max_length=7,
        default='#667eea',
        help_text='Color del evento en formato hexadecimal'
    )
    
    creado_en = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creación del evento'
    )
    
    actualizado_en = models.DateTimeField(
        auto_now=True,
        help_text='Última actualización del evento'
    )
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha_inicio']
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio.date()}"