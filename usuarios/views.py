from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods

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
            if user.activo:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.get_full_name() or user.username}!')
                return redirect('dashboard')  # Cambiar a la URL de tu dashboard
            else:
                messages.error(request, 'Tu cuenta ha sido desactivada. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'usuarios/login.html')


@login_required(login_url='login')
def dashboard_view(request):
    """
    Vista del dashboard para residentes autenticados.
    """
    context = {
        'usuario': request.user,
    }
    return render(request, 'usuarios/dashboard.html', context)


def logout_view(request):
    """
    Vista para cerrar sesión del usuario.
    """
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')
