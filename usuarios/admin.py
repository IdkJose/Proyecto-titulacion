from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Evento, Solicitud, Mascota
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del modelo Usuario en el panel de administración.
    """
    # Campos que se muestran en la lista de usuarios
    list_display = ['username', 'email', 'casa_departamento', 'rol', 'is_active', 'fecha_registro']
    
    # Filtros en la barra lateral
    list_filter = ['rol', 'is_active', 'is_staff', 'fecha_registro']
    
    # Campos por los que se puede buscar
    search_fields = ['username', 'email', 'first_name', 'last_name', 'casa_departamento']
    
    # Campos editables desde la lista
    list_editable = ['is_active']
    
    # Campos de solo lectura (no editables)
    readonly_fields = ['fecha_registro', 'last_login', 'date_joined']
    
    # Orden por defecto
    ordering = ['casa_departamento', 'last_name']
    
    # Configuración de los fieldsets (cómo se agrupan los campos al editar)
    fieldsets = (
        ('Credenciales', {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Información del Conjunto', {
            'fields': ('casa_departamento', 'telefono', 'rol', 'foto_perfil')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
            'description': 'Controla el acceso y permisos del usuario en el sistema.'
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined', 'fecha_registro'),
            'classes': ('collapse',)  # Esto hace que la sección esté colapsada por defecto
        }),
    )
    
    # Campos al crear un nuevo usuario
    add_fieldsets = (
        ('Credenciales', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Información Personal', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email'),
        }),
        ('Información del Conjunto', {
            'classes': ('wide',),
            'fields': ('casa_departamento', 'telefono', 'rol', 'foto_perfil'),
        }),
    )


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Evento en el panel de administración.
    """
    list_display = ['titulo', 'usuario', 'fecha_inicio', 'fecha_fin', 'color']
    list_filter = ['usuario', 'fecha_inicio', 'color']
    search_fields = ['titulo', 'descripcion', 'usuario__username']
    readonly_fields = ['creado_en', 'actualizado_en']
    
    fieldsets = (
        ('Información del Evento', {
            'fields': ('usuario', 'titulo', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Personalizacion', {
            'fields': ('color',)
        }),
        ('Timestamps', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Solicitud en el panel de administración.
    """
    list_display = ['titulo', 'usuario', 'tipo', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'tipo', 'fecha_creacion', 'usuario']
    search_fields = ['titulo', 'descripcion', 'usuario__username', 'usuario__email']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información de la Solicitud', {
            'fields': ('usuario', 'tipo', 'titulo', 'descripcion')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Respuesta del Administrador', {
            'fields': ('respuesta_admin',)
        }),
        ('Timestamps', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Mascota en el panel de administración.
    """
    list_display = ['nombre', 'tipo', 'numero_casa', 'dueno', 'fecha_registro', 'activo']
    list_filter = ['tipo', 'activo', 'fecha_registro', 'numero_casa']
    search_fields = ['nombre', 'dueno', 'numero_casa', 'descripcion']
    readonly_fields = ['fecha_registro']
    list_editable = ['activo']
    
    fieldsets = (
        ('Información de la Mascota', {
            'fields': ('nombre', 'tipo', 'descripcion')
        }),
        ('Información del Propietario', {
            'fields': ('dueno', 'numero_casa')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Timestamps', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )