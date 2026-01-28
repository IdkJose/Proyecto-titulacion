from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('solicitudes/crear/', views.crear_solicitud, name='crear_solicitud'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('crear_evento/', views.crear_evento, name='crear_evento'),
    path('mascotas/crear/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/obtener/<int:mascota_id>/', views.obtener_mascota, name='obtener_mascota'),
    path('mascotas/editar/<int:mascota_id>/', views.editar_mascota, name='editar_mascota'),
    path('mascotas/eliminar/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
]
