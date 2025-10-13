from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Usuario, PerfilUsuario
from .forms import FormularioRegistro, FormularioLogin, FormularioPerfil, FormularioConfiguracion


def registro(request):
    """
    Vista para registro de nuevos usuarios.
    """
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='usuarios.backends.EmailBackend')
            messages.success(
                request,
                f'¡Bienvenido {user.get_nombre_completo()}! '
                'Tu cuenta ha sido creada exitosamente.'
            )
            return redirect('index')
    else:
        form = FormularioRegistro()
    
    context = {
        'form': form,
        'titulo': 'Registro de Usuario'
    }
    
    return render(request, 'usuarios/registro.html', context)


def login_view(request):
    """
    Vista para login de usuarios.
    """
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = FormularioLogin(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # El backend se encarga de buscar por username o email
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user, backend='usuarios.backends.EmailBackend')
                
                if not remember_me:
                    request.session.set_expiry(0)  # Sesión temporal
                else:
                    request.session.set_expiry(1209600)  # 2 semanas
                
                messages.success(
                    request,
                    f'¡Bienvenido {user.get_nombre_completo()}!'
                )
                
                # Redirigir a la página solicitada o al dashboard
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Credenciales inválidas.')
    else:
        form = FormularioLogin()
    
    context = {
        'form': form,
        'titulo': 'Iniciar Sesión'
    }
    
    return render(request, 'usuarios/login.html', context)


@login_required
def logout_view(request):
    """
    Vista para cerrar sesión.
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


@login_required
def perfil(request):
    """
    Vista para ver y editar perfil de usuario.
    """
    usuario = request.user
    perfil, created = PerfilUsuario.objects.get_or_create(
        usuario=usuario,
        defaults={
            'tema_preferido': 'light',
            'plazos_por_pagina': 20,
            'idioma': 'es',
            'zona_horaria': 'America/Santiago',
            'notificaciones_email': True,
            'notificaciones_push': True,
            'recordar_filtros': True,
        }
    )
    
    if request.method == 'POST':
        form_perfil = FormularioPerfil(request.POST, instance=usuario)
        form_config = FormularioConfiguracion(request.POST, instance=perfil)
        
        if form_perfil.is_valid() and form_config.is_valid():
            try:
                form_perfil.save()
                form_config.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('perfil')
            except Exception as e:
                messages.error(request, f'Error al guardar: {str(e)}')
                print(f"Error al guardar perfil: {str(e)}")  # Debug en consola
        else:
            # Mostrar errores de validación
            if not form_perfil.is_valid():
                for field, errors in form_perfil.errors.items():
                    for error in errors:
                        messages.error(request, f'Error en {field}: {error}')
            if not form_config.is_valid():
                for field, errors in form_config.errors.items():
                    for error in errors:
                        messages.error(request, f'Error en configuración {field}: {error}')
    else:
        form_perfil = FormularioPerfil(instance=usuario)
        form_config = FormularioConfiguracion(instance=perfil)
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
        'form_perfil': form_perfil,
        'form_config': form_config,
        'titulo': 'Mi Perfil'
    }
    
    return render(request, 'usuarios/perfil.html', context)


@login_required
def cambiar_password(request):
    """
    Vista para cambiar contraseña.
    """
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmar = request.POST.get('password_confirmar')
        
        # Verificar contraseña actual
        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('cambiar_password')
        
        # Verificar que las nuevas contraseñas coincidan
        if password_nueva != password_confirmar:
            messages.error(request, 'Las contraseñas nuevas no coinciden.')
            return redirect('cambiar_password')
        
        # Verificar longitud mínima
        if len(password_nueva) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('cambiar_password')
        
        # Cambiar contraseña
        request.user.set_password(password_nueva)
        request.user.save()
        
        # Reautenticar al usuario
        login(request, request.user)
        
        messages.success(request, 'Contraseña cambiada exitosamente.')
        return redirect('perfil')
    
    return render(request, 'usuarios/cambiar_password.html', {'titulo': 'Cambiar Contraseña'})


@login_required
def lista_usuarios(request):
    """
    Vista para listar usuarios (solo administradores).
    """
    if not request.user.es_administrador():
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('index')
    
    # Filtros
    busqueda = request.GET.get('busqueda', '')
    tipo_usuario = request.GET.get('tipo_usuario', '')
    especialidad = request.GET.get('especialidad', '')
    
    usuarios = Usuario.objects.all()
    
    if busqueda:
        usuarios = usuarios.filter(
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda) |
            Q(username__icontains=busqueda) |
            Q(email__icontains=busqueda) |
            Q(rut__icontains=busqueda)
        )
    
    if tipo_usuario:
        usuarios = usuarios.filter(tipo_usuario=tipo_usuario)
    
    if especialidad:
        usuarios = usuarios.filter(especialidad=especialidad)
    
    usuarios = usuarios.order_by('last_name', 'first_name')
    
    # Paginación
    paginator = Paginator(usuarios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'busqueda': busqueda,
        'tipo_usuario': tipo_usuario,
        'especialidad': especialidad,
        'titulo': 'Gestión de Usuarios'
    }
    
    return render(request, 'usuarios/lista_usuarios.html', context)


@login_required
def detalle_usuario(request, usuario_id):
    """
    Vista para ver detalle de un usuario.
    """
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    # Solo el propio usuario o administradores pueden ver el perfil
    if not (request.user == usuario or request.user.es_administrador()):
        messages.error(request, 'No tienes permisos para ver este perfil.')
        return redirect('index')
    
    context = {
        'usuario_detalle': usuario,
        'perfil': usuario.perfil,
        'titulo': f'Perfil de {usuario.get_nombre_completo()}'
    }
    
    return render(request, 'usuarios/detalle_usuario.html', context)


@login_required
def toggle_usuario_activo(request, usuario_id):
    """
    Vista AJAX para activar/desactivar usuario.
    """
    if not request.user.es_administrador():
        return JsonResponse({'error': 'No tienes permisos para realizar esta acción.'})
    
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=usuario_id)
        usuario.es_activo = not usuario.es_activo
        usuario.save()
        
        estado = 'activado' if usuario.es_activo else 'desactivado'
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario {estado} exitosamente.',
            'activo': usuario.es_activo
        })
    
    return JsonResponse({'error': 'Método no permitido.'})


def verificar_rut(request):
    """
    Vista AJAX para verificar si un RUT ya existe.
    """
    if request.method == 'GET':
        rut = request.GET.get('rut', '')
        
        if rut:
            existe = Usuario.objects.filter(rut=rut).exists()
            return JsonResponse({'existe': existe})
    
    return JsonResponse({'existe': False})


def verificar_email(request):
    """
    Vista AJAX para verificar si un email ya existe.
    """
    if request.method == 'GET':
        email = request.GET.get('email', '')
        
        if email:
            existe = Usuario.objects.filter(email=email).exists()
            return JsonResponse({'existe': existe})
    
    return JsonResponse({'existe': False})

