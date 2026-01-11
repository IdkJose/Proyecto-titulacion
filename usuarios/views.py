from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from datetime import datetime
import calendar
from .models import Evento


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vista de login para residentes del conjunto.
    Permite autenticación con username y contraseña.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Si el usuario existe y está activo
            if user.is_active:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.get_full_name() or user.username}!')
                return redirect('usuarios:dashboard')  
            else:
                messages.error(request, 'Tu cuenta ha sido desactivada. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'usuarios/login.html')


@login_required(login_url='usuarios:login')
def dashboard_view(request):
    """
    Vista del dashboard para residentes autenticados.
    Muestra información del usuario y calendario con eventos.
    """
    today = datetime.now()
    mes = int(request.GET.get('mes', today.month))
    ano = int(request.GET.get('ano', today.year))
    
    # Generar calendario del mes
    cal = calendar.monthcalendar(ano, mes)
    
    # Obtener eventos del usuario para este mes
    eventos = Evento.objects.filter(
        usuario=request.user,
        fecha_inicio__year=ano,
        fecha_inicio__month=mes
    )
    
    # Crear diccionario {día: [eventos]}
    eventos_por_dia = {}
    for evento in eventos:
        dia = evento.fecha_inicio.day
        if dia not in eventos_por_dia:
            eventos_por_dia[dia] = []
        eventos_por_dia[dia].append(evento)
    
    # Calcular mes anterior y siguiente
    if mes == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes - 1
        ano_anterior = ano
    
    if mes == 12:
        mes_siguiente = 1
        ano_siguiente = ano + 1
    else:
        mes_siguiente = mes + 1
        ano_siguiente = ano
    
    # Nombres de meses
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    context = {
        'usuario': request.user,
        'calendario': cal,
        'eventos_por_dia': eventos_por_dia,
        'mes': mes,
        'ano': ano,
        'mes_nombre': meses[mes - 1],
        'mes_anterior': mes_anterior,
        'ano_anterior': ano_anterior,
        'mes_siguiente': mes_siguiente,
        'ano_siguiente': ano_siguiente,
    }
    
    # Usar template diferente según el rol del usuario
    if request.user.es_administrador():
        template = 'usuarios/dashboard_admin.html'
    else:
        template = 'usuarios/dashboard.html'
    
    return render(request, template, context)


def logout_view(request):
    """
    Vista para cerrar sesión del usuario.
    """
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('usuarios:login')