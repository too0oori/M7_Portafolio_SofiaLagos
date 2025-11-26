from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Direccion

class RegistroForm(forms.ModelForm):
    """
    Formulario de registro de usuarios
    """
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )
    password_confirm = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Usuario',
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Elige un nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu apellido'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        if password and len(password) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        
        return password_confirm


class PerfilForm(forms.ModelForm):
    """
    Formulario para editar el perfil del usuario
    """
    # Campos del User
    first_name = forms.CharField(
        label='Nombre',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    
    class Meta:
        model = Perfil
        fields = ['telefono', 'fecha_nacimiento', 'avatar']
        labels = {
            'telefono': 'Teléfono',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'avatar': 'Foto de perfil',
        }
        widgets = {
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prellenar campos del User
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        perfil = super().save(commit=False)
        
        # Actualizar campos del User
        user = perfil.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            perfil.save()
        
        return perfil


class DireccionForm(forms.ModelForm):
    """
    Formulario para agregar/editar direcciones
    """
    class Meta:
        model = Direccion
        fields = ['alias', 'calle', 'numero', 'comuna', 'ciudad', 'region', 'codigo_postal']
        labels = {
            'alias': 'Nombre de la dirección',
            'calle': 'Calle',
            'numero': 'Número',
            'comuna': 'Comuna',
            'ciudad': 'Ciudad',
            'region': 'Región',
            'codigo_postal': 'Código postal',
        }
        widgets = {
            'alias': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Casa, Trabajo, Casa de mis padres'
            }),
            'calle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la calle'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234'
            }),
            'comuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Santiago Centro'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Santiago'
            }),
            'region': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'Selecciona una región'),
                ('Región Metropolitana', 'Región Metropolitana'),
                ('Región de Valparaíso', 'Región de Valparaíso'),
                ('Región del Biobío', 'Región del Biobío'),
                ('Región de La Araucanía', 'Región de La Araucanía'),
                ('Región de Los Lagos', 'Región de Los Lagos'),
                ('Región de Antofagasta', 'Región de Antofagasta'),
                ('Región de Coquimbo', 'Región de Coquimbo'),
                ('Región de O\'Higgins', 'Región de O\'Higgins'),
                ('Región del Maule', 'Región del Maule'),
                ('Región de Ñuble', 'Región de Ñuble'),
                ('Región de Los Ríos', 'Región de Los Ríos'),
                ('Región de Aysén', 'Región de Aysén'),
                ('Región de Magallanes', 'Región de Magallanes'),
                ('Región de Arica y Parinacota', 'Región de Arica y Parinacota'),
                ('Región de Tarapacá', 'Región de Tarapacá'),
                ('Región de Atacama', 'Región de Atacama'),
            ]),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '8320000'
            }),
        }