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
    
    # Mensajería / Chat
    path('mensajes/', views.lista_chats, name='lista_chats'),
    path('mensajes/chat/<int:user_id>/', views.chat_con_usuario, name='chat_con_usuario'),
    path('mensajes/enviar-ajax/', views.enviar_mensaje_ajax, name='enviar_mensaje_ajax'),
    path('mensajes/obtener-ajax/<int:user_id>/', views.obtener_mensajes_ajax, name='obtener_mensajes_ajax'),
]
