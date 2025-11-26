
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Perfil, Direccion
from .forms import RegistroForm, PerfilForm, DireccionForm

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Crear perfil manualmente 
            Perfil.objects.create(user=user)
            
            login(request, user)
            messages.success(request, f'¡Bienvenido a A Medias Tintas, {user.username}!')
            return redirect('home')
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    """
    Vista de login de usuarios
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de vuelta, {user.username}!')
            
            # Redirigir  a home
            return redirect('apps.productos:home')
            
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'usuarios/login.html')


@login_required
def logout_view(request):
    """
    Vista de logout 
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('apps.productos:home')


@login_required
def perfil_view(request):
    """
    Vista del perfil del usuario 
    Muestra información del usuario, perfil y direcciones
    """
    perfil = request.user.perfil
    direcciones = request.user.direcciones.all()
    
    context = {
        'perfil': perfil,
        'direcciones': direcciones,
    }
    return render(request, 'usuarios/perfil.html', context)


class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para editar el perfil del usuario
    """
    model = Perfil
    form_class = PerfilForm
    template_name = 'usuarios/editar_perfil.html'
    success_url = reverse_lazy('perfil')
    
    def get_object(self):
        # Obtener el perfil del usuario actual
        return self.request.user.perfil
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)


@login_required
def agregar_direccion_view(request):
    """
    Vista para agregar una nueva dirección
    """
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.user = request.user
            direccion.save()
            messages.success(request, 'Dirección agregada correctamente.')
            return redirect('perfil')
    else:
        form = DireccionForm()
    
    return render(request, 'usuarios/agregar_direccion.html', {'form': form})


@login_required
def editar_direccion_view(request, pk):
    """
    Vista para editar una dirección existente
    """
    direccion = get_object_or_404(Direccion, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dirección actualizada correctamente.')
            return redirect('perfil')
    else:
        form = DireccionForm(instance=direccion)
    
    return render(request, 'usuarios/editar_direccion.html', {
        'form': form,
        'direccion': direccion
    })


@login_required
def eliminar_direccion_view(request, pk):
    """
    Vista para eliminar una dirección 
    """
    direccion = get_object_or_404(Direccion, pk=pk, user=request.user)
    
    if request.method == 'POST':
        direccion.delete()
        messages.success(request, 'Dirección eliminada correctamente.')
        return redirect('perfil')
    
    return render(request, 'usuarios/eliminar_direccion.html', {'direccion': direccion})