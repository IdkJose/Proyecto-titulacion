from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

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
        help_text='Correo electrÃ³nico del usuario'
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
                message='El telÃ©fono solo puede contener nÃºmeros'
            )
        ],
        help_text='NÃºmero de telÃ©fono del usuario'
    )
    
    casa_departamento = models.CharField(
        max_length=14,
        blank=False,
        null=False,
        help_text='NÃºmero de casa o departamento (ej: Casa 15, Depto 3B)'
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
        help_text='Indica si el usuario estÃ¡ activo en el conjunto'
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
        """RepresentaciÃ³n en string del usuario"""
        if self.casa_departamento:
            return f"{self.get_full_name()} - {self.casa_departamento}"
        return self.get_full_name() or self.username
    
    def es_administrador(self):
        """MÃ©todo helper para verificar si el usuario es administrador"""
        return self.rol == 'admin' or self.is_superuser


class Evento(models.Model):
    """
    Modelo para guardar eventos del calendario.
    Cada evento pertenece a un usuario especÃ­fico.
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='eventos',
        help_text='Usuario propietario del evento'
    )
    
    titulo = models.CharField(
        max_length=200,
        help_text='TÃ­tulo del evento'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text='DescripciÃ³n detallada del evento'
    )
    
    fecha_inicio = models.DateTimeField(
        help_text='Fecha y hora de inicio del evento'
    )
    
    fecha_fin = models.DateTimeField(
        help_text='Fecha y hora de fin del evento'
    )
    
    # Choices para categorÃ­as de eventos
    CATEGORIAS = [
        ('minga', 'Minga'),
        ('reunion', 'ReuniÃ³n'),
        ('mantenimiento', 'Mantenimiento'),
        ('evento_social', 'Evento Social'),
        ('otro', 'Otro'),
    ]
    
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default='otro',
        help_text='CategorÃ­a del evento'
    )
    
    color = models.CharField(
        max_length=7,
        default='#667eea',
        help_text='Color del evento en formato hexadecimal'
    )
    
    creado_en = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creaciÃ³n del evento'
    )
    
    actualizado_en = models.DateTimeField(
        auto_now=True,
        help_text='Ãšltima actualizaciÃ³n del evento'
    )
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha_inicio']
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio.date()}"


class Solicitud(models.Model):
    """
    Modelo para gestionar solicitudes de residentes.
    Los vecinos pueden crear solicitudes para diferentes trÃ¡mites.
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
        help_text='DescripciÃ³n detallada de la solicitud'
    )
    
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='pendiente',
        help_text='Estado actual de la solicitud'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creaciÃ³n de la solicitud'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text='Ãšltima actualizaciÃ³n de la solicitud'
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
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo} ({self.get_estado_display()})"


class Mascota(models.Model):
    """
    Modelo para registrar mascotas que habitan en el conjunto.
    Cada mascota estÃ¡ asociada a una casa/departamento.
    """
    
    TIPO_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('pajaro', 'PÃ¡jaro'),
        ('conejo', 'Conejo'),
        ('hamster', 'HÃ¡mster'),
        ('otro', 'Otro'),
    ]
    
    numero_casa = models.CharField(
        max_length=14,
        help_text='NÃºmero de casa o departamento donde reside la mascota'
    )
    
    nombre = models.CharField(
        max_length=100,
        help_text='Nombre de la mascota'
    )
    
    dueno = models.CharField(
        max_length=200,
        help_text='Nombre del dueÃ±o de la mascota'
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
        help_text='DescripciÃ³n adicional de la mascota (color, caracterÃ­sticas, etc)'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de registro de la mascota'
    )
    
    activo = models.BooleanField(
        default=True,
        help_text='Indica si el registro de la mascota estÃ¡ activo'
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
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()}) - {self.numero_casa}"


class Mensaje(models.Model):
    """
    Modelo para los mensajes del chat entre AdministraciÃ³n y Residentes.
    """
    remitente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='mensajes_enviados',
        help_text='Usuario que envÃ­a el mensaje'
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
        help_text='Indica si el mensaje ha sido leÃ­do por el destinatario'
    )
    
    fecha_envio = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora en que se enviÃ³ el mensaje'
    )
    
    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['fecha_envio']
    
    def __str__(self):
        return f"De: {self.remitente} Para: {self.destinatario} - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"
class Publicacion(models.Model):
    """
    Modelo para gestionar comunicados, noticias y reportes (estados de cuenta).
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

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo} ({self.fecha_publicacion.date()})"

