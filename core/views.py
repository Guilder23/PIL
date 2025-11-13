from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages

from .forms import RegistroUsuarioForm
from .models import PerfilUsuario

# Create your views here.

def home(request):
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente.')
            return redirect('dashboard')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def dashboard(request):
    perfil = getattr(request.user, 'perfil', None)
    role = getattr(perfil, 'role', None)
    if role == 'ADMIN':
        return redirect('dashboard_admin')
    elif role == 'CLIENTE':
        return redirect('dashboard_cliente')
    elif role == 'CHOFER':
        return redirect('dashboard_chofer')
    # fallback si no tiene perfil
    return render(request, 'dashboard/generico.html')

@login_required
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html')

@login_required
def dashboard_cliente(request):
    return render(request, 'dashboard/cliente.html')

@login_required
def dashboard_chofer(request):
    return render(request, 'dashboard/chofer.html')

def _is_admin(user):
    perfil = getattr(user, 'perfil', None)
    return user.is_authenticated and getattr(perfil, 'role', None) == PerfilUsuario.ADMIN

# Decorador para restringir vistas a ADMIN
admin_required = user_passes_test(_is_admin, login_url='login')

@login_required
@admin_required
def usuarios_list(request):
    from django.contrib.auth.models import User
    users = User.objects.all()
    users_ctx = []
    for u in users:
        perfil = getattr(u, 'perfil', None)
        role = getattr(perfil, 'role', None)
        users_ctx.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'is_active': u.is_active,
            'role': role,
        })
    return render(request, 'users/list.html', { 'users_ctx': users_ctx })

@login_required
@admin_required
def usuarios_create(request):
    from .forms import AdminUserCreateForm
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('usuarios_list')
    else:
        form = AdminUserCreateForm()
    return render(request, 'users/form.html', { 'form': form, 'accion': 'Crear usuario' })

@login_required
@admin_required
def usuarios_update(request, user_id):
    from django.contrib.auth.models import User
    from .forms import AdminUserUpdateForm
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios_list')
    else:
        form = AdminUserUpdateForm(instance=user)
    return render(request, 'users/form.html', { 'form': form, 'accion': 'Editar usuario' })

@login_required
@admin_required
def usuarios_delete(request, user_id):
    from django.contrib.auth.models import User
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Usuario "{username}" eliminado.')
        return redirect('usuarios_list')
    return render(request, 'users/confirm_delete.html', { 'user_obj': user })

@login_required
@admin_required
def usuarios_change_password(request, user_id):
    from django.contrib.auth.models import User
    from .forms import AdminUserPasswordForm
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = AdminUserPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('usuarios_list')
    else:
        form = AdminUserPasswordForm()
    return render(request, 'users/change_password.html', { 'form': form, 'user_obj': user })
