from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('solicitudes/crear/', views.crear_solicitud, name='crear_solicitud'),
    path('solicitudes/gestionar/<int:solicitud_id>/', views.gestionar_solicitud, name='gestionar_solicitud'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('crear_evento/', views.crear_evento, name='crear_evento'),
    path('mascotas/crear/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/obtener/<int:mascota_id>/', views.obtener_mascota, name='obtener_mascota'),
    path('mascotas/editar/<int:mascota_id>/', views.editar_mascota, name='editar_mascota'),
    path('mascotas/eliminar/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
    # Publicaciones (Comunicados/Reportes)
    path('publicaciones/crear/', views.crear_publicacion, name='crear_publicacion'),
    path('publicaciones/editar/<int:pk>/', views.editar_publicacion, name='editar_publicacion'),
    path('publicaciones/eliminar/<int:pk>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('vehiculos/crear/', views.crear_vehiculo, name='crear_vehiculo'),
    path('vehiculos/obtener/<int:vehiculo_id>/', views.obtener_vehiculo, name='obtener_vehiculo'),
    path('vehiculos/editar/<int:vehiculo_id>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
]
