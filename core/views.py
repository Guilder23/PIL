from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .forms import RegistroUsuarioForm

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
