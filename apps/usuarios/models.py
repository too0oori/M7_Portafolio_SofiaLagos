from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# usuarios/models.py

class Perfil(models.Model):
    """Extensión del User de Django - Relación 1:1"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatares/', null=True, blank=True)

class Direccion(models.Model):
    """Direcciones de envío del usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direcciones')
    alias = models.CharField(max_length=50)  # "Casa", "Trabajo"
    calle = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    comuna = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)