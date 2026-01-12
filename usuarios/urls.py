from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
]
