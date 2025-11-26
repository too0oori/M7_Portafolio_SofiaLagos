from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    """Extensión del User de Django - Relación 1:1"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatares/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

class Direccion(models.Model):
    """Direcciones de envío del usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direcciones')
    alias = models.CharField(max_length=50)
    calle = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    comuna = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
    
    def __str__(self):
        return f"{self.alias} - {self.user.username}"
