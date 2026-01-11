from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Evento
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del modelo Usuario en el panel de administración.
    """
    # Campos que se muestran en la lista de usuarios
    list_display = ['username', 'email', 'casa_departamento', 'rol', 'activo', 'fecha_registro']
    
    # Filtros en la barra lateral
    list_filter = ['rol', 'activo', 'is_staff', 'fecha_registro']
    
    # Campos por los que se puede buscar
    search_fields = ['username', 'email', 'first_name', 'last_name', 'casa_departamento']
    
    # Campos editables desde la lista
    list_editable = ['activo']
    
    # Orden por defecto
    ordering = ['casa_departamento', 'last_name']
    
    # Configuración de los fieldsets (cómo se agrupan los campos al editar)
    fieldsets = UserAdmin.fieldsets + (
        ('Información del Conjunto', {
            'fields': ('casa_departamento', 'telefono', 'rol', 'foto_perfil', 'activo')
        }),
    )
    
    # Campos al crear un nuevo usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información del Conjunto', {
            'fields': ('casa_departamento', 'telefono', 'rol', 'foto_perfil')
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