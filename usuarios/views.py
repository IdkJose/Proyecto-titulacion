from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .forms import UsuarioCreationForm, UsuarioChangeForm, EventoForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.utils import timezone
import calendar
from .models import Evento, Solicitud, Usuario, Mascota, Publicacion, Vehiculo


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vista de login para residentes del conjunto.
    Permite autenticación con username y contraseña.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Primero verificar si el usuario existe
        try:
            usuario_existente = Usuario.objects.get(username=username)
            
            # Si existe pero está inactivo, mostrar mensaje específico
            if not usuario_existente.is_active:
                messages.error(request, 'Usuario inactivo. Comuníquese con el administrador.')
                return render(request, 'usuarios/login.html')
        except Usuario.DoesNotExist:
            pass  # Si no existe, continuar con autenticación normal
        
        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.get_full_name() or user.username}!')
            return redirect('usuarios:dashboard')  
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
    
    # Obtener solicitudes según el rol
    if request.user.es_administrador():
        solicitudes = Solicitud.objects.all().order_by('-fecha_creacion')
        # Contador de solicitudes pendientes para el administrador
        solicitudes_pendientes_count = solicitudes.filter(estado='pendiente').count()
    else:
        solicitudes = Solicitud.objects.filter(usuario=request.user).order_by('-fecha_creacion')
        solicitudes_pendientes_count = 0
    
    # Obtener mascotas registradas
    mascotas = Mascota.objects.filter(activo=True)
    
    # Obtener vehículos del usuario
    vehiculos = Vehiculo.objects.filter(usuario=request.user)
    
    # Obtener lista de vecinos (todos los usuarios activos excepto el actual)
    # Ordenados por casa/departamento
    vecinos = Usuario.objects.filter(activo=True).exclude(id=request.user.id).order_by('casa_departamento', 'last_name')
    
    # Obtener publicaciones (noticias/reportes)
    publicaciones = Publicacion.objects.all().order_by('-fecha_publicacion')
    
    # Obtener el primer administrador para que los residentes puedan chatear
    primer_admin = Usuario.objects.filter(rol='admin', activo=True).first()

    context = {
        'usuario': request.user,
        'calendario': cal,
        'eventos_por_dia': eventos_por_dia,
        'solicitudes': solicitudes,
        'solicitudes_pendientes_count': solicitudes_pendientes_count,
        'mascotas': mascotas,
        'vehiculos': vehiculos,
        'vecinos': vecinos,
        'publicaciones': publicaciones,
        'primer_admin': primer_admin,
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
        template = 'usuarios/dashboard_residente.html'
    
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
@require_http_methods(["POST"])
def crear_publicacion(request):
    """
    Crea una nueva publicación (comunicado o reporte).
    """
    titulo = request.POST.get('titulo')
    contenido = request.POST.get('contenido')
    tipo = request.POST.get('tipo', 'comunicado')
    imagen = request.FILES.get('imagen')
    archivo_pdf = request.FILES.get('archivo_pdf')
    
    try:
        Publicacion.objects.create(
            autor=request.user,
            titulo=titulo,
            contenido=contenido,
            tipo=tipo,
            imagen=imagen,
            archivo_pdf=archivo_pdf
        )
        messages.success(request, '¡Publicación creada con éxito, pana! 🚀')
    except Exception as e:
        messages.error(request, f'Chuta, algo salió mal: {str(e)}')
        
    return redirect('usuarios:dashboard')


@login_required
@user_passes_test(lambda u: u.es_administrador())
@require_http_methods(["POST"])
def editar_publicacion(request, pk):
    """
    Edita una publicación existente.
    """
    publicacion = get_object_or_404(Publicacion, pk=pk)
    
    publicacion.titulo = request.POST.get('titulo', publicacion.titulo)
    publicacion.contenido = request.POST.get('contenido', publicacion.contenido)
    publicacion.tipo = request.POST.get('tipo', publicacion.tipo)
    
    if 'imagen' in request.FILES:
        publicacion.imagen = request.FILES['imagen']
    if 'archivo_pdf' in request.FILES:
        publicacion.archivo_pdf = request.FILES['archivo_pdf']
        
    try:
        publicacion.save()
        messages.success(request, '¡Publicación actualizada! Todo bien. ✅')
    except Exception as e:
        messages.error(request, f'No se pudo actualizar: {str(e)}')
        
    return redirect('usuarios:dashboard')


@login_required
@user_passes_test(lambda u: u.es_administrador())
@require_http_methods(["POST"])
def eliminar_publicacion(request, pk):
    """
    Elimina una publicación.
    """
    publicacion = get_object_or_404(Publicacion, pk=pk)
    try:
        publicacion.delete()
        messages.success(request, 'Publicación eliminada correctamente. 👍')
    except Exception as e:
        messages.error(request, f'No se pudo eliminar la nota: {str(e)}')
        
    return redirect('usuarios:dashboard')


@login_required(login_url='usuarios:login')
@require_http_methods(["POST"])
def crear_solicitud(request):
    """
    Vista para crear una nueva solicitud.
    """
    tipo = request.POST.get('tipo')
    titulo = request.POST.get('titulo')
    descripcion = request.POST.get('descripcion')
    
    if tipo and titulo and descripcion:
        Solicitud.objects.create(
            usuario=request.user,
            tipo=tipo,
            titulo=titulo,
            descripcion=descripcion
        )
        messages.success(request, '¡Solicitud creada exitosamente!')
    else:
        messages.error(request, 'Por favor completa todos los campos.')
    
    return redirect('usuarios:dashboard')


@login_required
@user_passes_test(lambda u: u.es_administrador())
@require_http_methods(["POST"])
def gestionar_solicitud(request, solicitud_id):
    """
    Vista para que el administrador responda y cambie el estado de una solicitud.
    """
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    nuevo_estado = request.POST.get('estado')
    respuesta = request.POST.get('respuesta')
    
    if nuevo_estado:
        solicitud.estado = nuevo_estado
        solicitud.respuesta_admin = respuesta
        solicitud.save()
        messages.success(request, f'✅ Solicitud #{solicitud.id} actualizada correctamente.')
    else:
        messages.error(request, 'Error al actualizar la solicitud.')
        
    return redirect('usuarios:dashboard')


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


@login_required
@require_http_methods(["POST"])
def crear_mascota(request):
    """
    Vista para crear un registro de mascota.
    Los vecinos pueden registrar mascotas dentro del conjunto.
    """
    try:
        numero_casa = request.POST.get('numero_casa', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        dueno = request.POST.get('dueno', '').strip()
        tipo = request.POST.get('tipo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        foto = request.FILES.get('foto', None)
        
        # Validar que todos los campos requeridos sean proporcionados
        if not all([numero_casa, nombre, dueno, tipo]):
            messages.error(request, 'Por favor completa todos los campos del formulario.')
            return redirect('usuarios:dashboard')
        
        # Crear la mascota
        mascota = Mascota(
            usuario=request.user,  
            numero_casa=numero_casa,
            nombre=nombre,
            dueno=dueno,
            tipo=tipo,
            descripcion=descripcion  
        )
        
        # Guardar foto 
        if foto:
            mascota.foto = foto
        
        mascota.save()
        foto_text = " con foto" if foto else ""
        messages.success(request, f'✅ Mascota "{nombre}" registrada exitosamente{foto_text}.')
    except Exception as e:
        messages.error(request, f'Error al registrar la mascota: {str(e)}')
    
    return redirect('usuarios:dashboard')


@login_required
@require_http_methods(["GET"])
def obtener_mascota(request, mascota_id):
    """
    Vista para obtener datos de una mascota en formato JSON.
    """
    try:
        mascota = Mascota.objects.get(id=mascota_id)
        data = {
            'id': mascota.id,
            'numero_casa': mascota.numero_casa,
            'nombre': mascota.nombre,
            'dueno': mascota.dueno,
            'tipo': mascota.tipo,
            'descripcion': mascota.descripcion or '',
        }
        return JsonResponse(data)
    except Mascota.DoesNotExist:
        return JsonResponse({'error': 'Mascota no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def editar_mascota(request, mascota_id):
    """
    Vista para editar una mascota existente.
    Solo el propietario puede editar su mascota (administrador puede editar cualquiera).
    """
    try:
        mascota = Mascota.objects.get(id=mascota_id)
        
        # Validar permisos: solo propietario o administrador
        if mascota.usuario != request.user and not request.user.es_administrador():
            messages.error(request, 'No tienes permiso para editar esta mascota.')
            return redirect('usuarios:dashboard')
        
        mascota.numero_casa = request.POST.get('numero_casa', '').strip() or mascota.numero_casa
        mascota.nombre = request.POST.get('nombre', '').strip() or mascota.nombre
        mascota.dueno = request.POST.get('dueno', '').strip() or mascota.dueno
        mascota.tipo = request.POST.get('tipo', '').strip() or mascota.tipo
        mascota.descripcion = request.POST.get('descripcion', '').strip()
        
        # Actualizar foto si se proporciona
        if 'foto' in request.FILES:
            mascota.foto = request.FILES['foto']
        
        mascota.save()
        messages.success(request, f'✅ Mascota "{mascota.nombre}" actualizada exitosamente.')
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no fue encontrada.')
    except Exception as e:
        messages.error(request, f'Error al actualizar la mascota: {str(e)}')
    
    return redirect('usuarios:dashboard')


@login_required
@require_http_methods(["POST"])
def eliminar_mascota(request, mascota_id):
    """
    Vista para eliminar una mascota.
    Solo el propietario puede eliminar su mascota (administrador puede eliminar cualquiera).
    """
    try:
        mascota = Mascota.objects.get(id=mascota_id)
        
        # Validar permisos: solo propietario o administrador
        if mascota.usuario != request.user and not request.user.es_administrador():
            messages.error(request, 'No tienes permiso para eliminar esta mascota.')
            return redirect('usuarios:dashboard')
        
        nombre = mascota.nombre
        mascota.delete()
        messages.success(request, f'✅ Mascota "{nombre}" eliminada exitosamente.')
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no fue encontrada.')
    except Exception as e:
        messages.error(request, f'Error al eliminar la mascota: {str(e)}')
    
    return redirect('usuarios:dashboard')


# ========== VISTAS DE VEHÍCULOS ==========

@login_required(login_url='usuarios:login')
@require_http_methods(["POST"])
def crear_vehiculo(request):
    """
    Vista para crear un nuevo vehículo registrado por el usuario.
    """
    try:
        numero_casa = request.POST.get('numero_casa')
        dueno = request.POST.get('dueno')
        placa = request.POST.get('placa')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        color = request.POST.get('color')
        
        # Validar que no exista otro vehículo con la misma placa
        if Vehiculo.objects.filter(placa=placa).exists():
            messages.error(request, f'❌ Ya existe un vehículo registrado con la placa {placa}.')
            return redirect('usuarios:dashboard')
        
        # Crear el vehículo
        vehiculo = Vehiculo.objects.create(
            usuario=request.user,
            numero_casa=numero_casa,
            dueno=dueno,
            placa=placa,
            marca=marca,
            modelo=modelo,
            color=color
        )
        
        messages.success(request, f'✅ Vehículo "{vehiculo.marca} {vehiculo.modelo}" ({placa}) registrado exitosamente.')
    except Exception as e:
        messages.error(request, f'❌ Error al registrar el vehículo: {str(e)}')
    
    return redirect('usuarios:dashboard')


# ========== VISTAS DE CHAT/MENSAJERÍA ==========

@login_required(login_url='usuarios:login')
def chat_view(request, user_id):
    """
    Vista del chat entre dos usuarios (residente y administrador).
    """
    from .models import Mensaje
    from django.db.models import Q
    
    otro_usuario = get_object_or_404(Usuario, id=user_id)
    
    # Obtener mensajes entre ambos usuarios
    mensajes = Mensaje.objects.filter(
        Q(remitente=request.user, destinatario=otro_usuario) |
        Q(remitente=otro_usuario, destinatario=request.user)
    ).order_by('fecha_envio')
    
    # Marcar como leídos los mensajes recibidos
    Mensaje.objects.filter(
        remitente=otro_usuario,
        destinatario=request.user,
        leido=False
    ).update(leido=True)
    
    context = {
        'otro_usuario': otro_usuario,
        'mensajes': mensajes,
    }
    
    return render(request, 'usuarios/chat.html', context)


@login_required(login_url='usuarios:login')
@require_http_methods(["POST"])
def enviar_mensaje_ajax(request):
    """
    Vista AJAX para enviar mensajes en el chat.
    """
    from .models import Mensaje
    
    contenido = request.POST.get('contenido', '').strip()
    destinatario_id = request.POST.get('destinatario_id')
    
    if not contenido or not destinatario_id:
        return JsonResponse({'status': 'error', 'mensaje': 'Datos incompletos'}, status=400)
    
    try:
        destinatario = Usuario.objects.get(id=destinatario_id)
        mensaje = Mensaje.objects.create(
            remitente=request.user,
            destinatario=destinatario,
            contenido=contenido
        )
        
        return JsonResponse({
            'status': 'ok',
            'mensaje': mensaje.contenido,
            'fecha': mensaje.fecha_envio.strftime('%H:%M')
        })
    except Usuario.DoesNotExist:
        return JsonResponse({'status': 'error', 'mensaje': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=500)


@login_required(login_url='usuarios:login')
@require_http_methods(["GET"])
def obtener_mensajes_ajax(request, user_id):
    """
    Vista AJAX para obtener nuevos mensajes no leídos.
    """
    from .models import Mensaje
    
    try:
        otro_usuario = Usuario.objects.get(id=user_id)
        
        # Obtener mensajes no leídos del otro usuario
        mensajes_nuevos = Mensaje.objects.filter(
            remitente=otro_usuario,
            destinatario=request.user,
            leido=False
        ).order_by('fecha_envio')
        
        # Marcarlos como leídos
        mensajes_nuevos.update(leido=True)
        
        # Serializar mensajes
        mensajes_data = [{
            'contenido': msg.contenido,
            'fecha': msg.fecha_envio.strftime('%H:%M'),
            'remitente': msg.remitente.get_full_name() or msg.remitente.username
        } for msg in mensajes_nuevos]
        
        return JsonResponse({'mensajes': mensajes_data})
    except Usuario.DoesNotExist:
        return JsonResponse({'mensajes': []}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='usuarios:login')
@user_passes_test(lambda u: u.es_administrador())
def lista_chats_admin(request):
    """
    Vista para que el administrador vea la lista de residentes con los que puede chatear.
    """
    # Obtener todos los residentes (usuarios que no son admin)
    residentes = Usuario.objects.filter(
        activo=True,
        rol='vecino'
    ).order_by('casa_departamento', 'last_name')
    
    # Para cada residente, obtener el conteo de mensajes no leídos
    from .models import Mensaje
    from django.db.models import Count, Q
    
    for residente in residentes:
        residente.mensajes_no_leidos = Mensaje.objects.filter(
            remitente=residente,
            destinatario=request.user,
            leido=False
        ).count()
    
    context = {
        'residentes': residentes,
    }
    
    return render(request, 'usuarios/lista_chats.html', context)
