from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UsuarioCreationForm, UsuarioChangeForm, EventoForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.utils import timezone
import calendar
from .models import Evento, Usuario


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
    # Obtener eventos del usuario O eventos de administradores (globales)
    # Filtramos por mes y año
    from django.db.models import Q
    eventos = Evento.objects.filter(
        Q(usuario=request.user) | Q(usuario__rol='admin'),
        fecha_inicio__year=ano,
        fecha_inicio__month=mes
    ).distinct()
    
    # Crear diccionario {día: [eventos]}
    eventos_por_dia = {}
    for evento in eventos:
        # Convertir a zona horaria local antes de obtener el día
        fecha_local = timezone.localtime(evento.fecha_inicio)
        dia = fecha_local.day
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


@login_required
@user_passes_test(lambda u: u.es_administrador())
def crear_usuario(request):
    """
    Vista para crear nuevos usuarios.
    Solo accesible para administradores.
    """
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.username} creado exitosamente.')
            return redirect('usuarios:dashboard')
    else:
        form = UsuarioCreationForm()
    
    return render(request, 'usuarios/crear_usuario.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.es_administrador())
def lista_usuarios(request):
    """
    Vista para listar todos los usuarios registrados.
    """
    usuarios = Usuario.objects.all().order_by('casa_departamento')
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})



@login_required
@user_passes_test(lambda u: u.es_administrador())
def editar_usuario(request, user_id):
    """
    Vista para editar un usuario existente.
    """
    usuario_editar = get_object_or_404(Usuario, id=user_id)
    
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, request.FILES, instance=usuario_editar)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {usuario_editar.username} actualizado exitosamente.')
            return redirect('usuarios:lista_usuarios')
    else:
        form = UsuarioChangeForm(instance=usuario_editar)
    
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario_editar': usuario_editar})


@login_required
@user_passes_test(lambda u: u.es_administrador())
def eliminar_usuario(request, user_id):
    """
    Vista para eliminar un usuario.
    No permite eliminar administradores.
    """
    usuario_eliminar = get_object_or_404(Usuario, id=user_id)
    
    # Verificar si es admin
    if usuario_eliminar.rol == 'admin':
        messages.error(request, 'No se puede eliminar a un usuario con rol de Administrador.')
        return redirect('usuarios:lista_usuarios')
    
    # Eliminar
    nombre = usuario_eliminar.username
    usuario_eliminar.delete()
    messages.success(request, f'Usuario {nombre} eliminado correctamente.')
    return redirect('usuarios:lista_usuarios')


@login_required
@user_passes_test(lambda u: u.es_administrador())
def crear_evento(request):
    """
    Vista para crear un evento en el calendario.
    Solo para administradores.
    """
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            messages.success(request, 'Evento creado exitosamente.')
            return redirect('usuarios:dashboard')
    else:
        # Pre-seleccionar fecha/hora actual
        form = EventoForm(initial={'fecha_inicio': datetime.now(), 'fecha_fin': datetime.now()})
    
    return render(request, 'usuarios/crear_evento.html', {'form': form})
