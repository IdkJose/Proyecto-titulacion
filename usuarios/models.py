from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

validador_ecuador = RegexValidator(
    regex=r'^09\d{8}$',
    message="El número de teléfono debe empezar con '09' y tener 10 dígitos en total (ej: 0991234567)."
)

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
# Modelo de Usuario Personalizado para el Conjunto Selva Alegre
class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    Agrega campos especÃ­ficos para vecinos del conjunto habitacional.
    """
    
    # Choices para el campo rol
    ROLES = [
        ('admin', 'Administrador'),
        ('vecino', 'Vecino'),
    ]
    
    objects = UsuarioManager()
    
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
        validators=[validador_ecuador],
        max_length=10, 
        help_text='El teléfono es obligatorio y debe tener un formato ecuatoriano válido.'
    )
    
    casa_departamento = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text='Número o identificador de la casa/departamento (ej: Casa 15, Dpto 3B)'
    )
    
    rol = models.CharField(
        max_length=20, 
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
        db_table = 'usuarios'
    
    def __str__(self):
        """Representación en string del usuario"""
        if self.casa_departamento:
            return f"{self.get_full_name()} - {self.casa_departamento}"
        return self.get_full_name() or self.username
    
    def es_administrador(self):
        """Método helper para verificar si el usuario es administrador"""
        return self.rol == 'admin' or self.is_superuser


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
        db_table = 'eventos'
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio.date()}"


class Solicitud(models.Model):
    """
    Modelo para gestionar solicitudes de residentes.
    Los vecinos pueden crear solicitudes para diferentes trámites.
    """
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    
    TIPO_CHOICES = [
        ('mantenimiento', 'Mantenimiento'),
        ('permiso', 'Permiso'),
        ('queja', 'Queja'),
        ('sugerencia', 'Sugerencia'),
        ('otro', 'Otro'),
    ]
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='solicitudes',
        help_text='Usuario que realiza la solicitud'
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='otro',
        help_text='Tipo de solicitud'
    )
    
    titulo = models.CharField(
        max_length=200,
        help_text='Asunto de la solicitud'
    )
    
    descripcion = models.TextField(
        help_text='Descripción detallada de la solicitud'
    )
    
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='pendiente',
        help_text='Estado actual de la solicitud'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creación de la solicitud'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text='Última actualización de la solicitud'
    )
    
    respuesta_admin = models.TextField(
        blank=True,
        null=True,
        help_text='Respuesta del administrador'
    )
    
    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        ordering = ['-fecha_creacion']
        db_table = 'solicitudes'
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo} ({self.get_estado_display()})"


class Mascota(models.Model):
    """
    Modelo para registrar mascotas que habitan en el conjunto.
    Cada mascota está asociada a una casa/departamento.
    """
    
    TIPO_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('pajaro', 'Pájaro'),
        ('conejo', 'Conejo'),
        ('hamster', 'Hámster'),
        ('otro', 'Otro'),
    ]
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='mascotas',
        null=True,
        blank=True,
        help_text='Usuario propietario de la mascota'
    )
    
    numero_casa = models.CharField(
        max_length=14,
        help_text='Número de casa o departamento donde reside la mascota'
    )
    
    nombre = models.CharField(
        max_length=100,
        help_text='Nombre de la mascota'
    )
    
    dueno = models.CharField(
        max_length=200,
        help_text='Nombre del dueño de la mascota'
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='otro',
        help_text='Tipo de mascota'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text='Descripción adicional de la mascota (color, características, etc)'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de registro de la mascota'
    )
    
    activo = models.BooleanField(
        default=True,
        help_text='Indica si el registro de la mascota está activo'
    )
    
    foto = models.ImageField(
        upload_to='mascotas/fotos/',
        blank=True,
        null=True,
        help_text='Foto de la mascota'
    )
    
    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['numero_casa', 'nombre']
        db_table = 'mascotas'
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()}) - {self.numero_casa}"


class Mensaje(models.Model):
    """
    Modelo para los mensajes del chat entre Administración y Residentes.
    """
    remitente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='mensajes_enviados',
        help_text='Usuario que envía el mensaje'
    )
    
    destinatario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='mensajes_recibidos',
        help_text='Usuario que recibe el mensaje'
    )
    
    contenido = models.TextField(
        help_text='Contenido del mensaje'
    )
    
    leido = models.BooleanField(
        default=False,
        help_text='Indica si el mensaje ha sido leído por el destinatario'
    )
    
    fecha_envio = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora en que se envió el mensaje'
    )
    
    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['fecha_envio']
        db_table = 'mensajes'
    
    def __str__(self):
        return f"De: {self.remitente} Para: {self.destinatario} - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"


class Vehiculo(models.Model):
    """
    Modelo para registrar vehículos de los residentes del conjunto.
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vehiculos',
        help_text='Usuario propietario del vehículo'
    )
    
    numero_casa = models.CharField(
        max_length=14,
        help_text='Número de casa o departamento (ej: Casa 15, Depto 3B)'
    )
    
    dueno = models.CharField(
        max_length=150,
        help_text='Nombre del propietario del vehículo'
    )
    
    placa = models.CharField(
        max_length=20,
        unique=True,
        help_text='Placa del vehículo (ej: ABC-1234)'
    )
    
    marca = models.CharField(
        max_length=100,
        help_text='Marca del vehículo (ej: Toyota, Honda)'
    )
    
    modelo = models.CharField(
        max_length=100,
        help_text='Modelo del vehículo (ej: Corolla, Civic)'
    )
    
    color = models.CharField(
        max_length=50,
        help_text='Color del vehículo'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora de registro del vehículo'
    )
    
    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering = ['-fecha_registro']
        db_table = 'vehiculos'
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"


class Publicacion(models.Model):
    """
    Modelo para los comunicados, novedades, finanzas y reportes de mantenimiento.
    """
    TIPO_CHOICES = [
        ('comunicado', '📢 Comunicado'),
        ('novedad', '✨ Novedad'),
        ('finanzas', '💰 Finanzas'),
        ('mantenimiento', '🛠️ Mantenimiento'),
    ]

    autor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='publicaciones',
        help_text='Administrador que crea la publicación'
    )
    titulo = models.CharField(
        max_length=200,
        help_text='Título corto y descriptivo'
    )
    contenido = models.TextField(
        help_text='Cuerpo del mensaje o noticia'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='comunicado',
        help_text='Categoría de la publicación'
    )
    imagen = models.ImageField(
        upload_to='publicaciones/imagenes/',
        blank=True,
        null=True,
        help_text='Imagen ilustrativa opcional'
    )
    archivo_pdf = models.FileField(
        upload_to='publicaciones/documentos/',
        blank=True,
        null=True,
        help_text='Documento adjunto (ej. Estado de Cuenta)'
    )
    fecha_publicacion = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha en que se hizo pública la nota'
    )

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-fecha_publicacion']
        db_table = 'publicaciones'

    def __str__(self):
        return self.titulo


class ReaccionSolicitud(models.Model):
    """
    Modelo para gestionar las reacciones (likes) en las solicitudes.
    Cada usuario puede reaccionar una sola vez a una solicitud.
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reacciones_solicitud',
        help_text='Usuario que reacciona'
    )
    solicitud = models.ForeignKey(
        Solicitud,
        on_delete=models.CASCADE,
        related_name='reacciones',
        help_text='Solicitud a la que se reacciona'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de la reacción'
    )

    class Meta:
        verbose_name = 'Reacción de Solicitud'
        verbose_name_plural = 'Reacciones de Solicitud'
        db_table = 'reacciones_solicitud'
        # Unicidad: un usuario solo puede reaccionar una vez por solicitud
        unique_together = ('usuario', 'solicitud')

    def __str__(self):
        return f"{self.usuario.username} reaccionó a {self.solicitud.titulo}"
