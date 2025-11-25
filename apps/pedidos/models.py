from django.db import models
from django.contrib.auth.models import User
from apps.usuarios.models import Direccion
from apps.productos.models import Producto, Talla

# Create your models here.
# pedidos/models.py

class Pedido(models.Model):
    """Orden de compra"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_proceso', 'En Proceso'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(User, on_delete=models.CASCADE) 
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    direccion_envio = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True)
    
    # Datos de envío
    direccion_completa = models.TextField()
    
    # Pago
    metodo_pago = models.CharField(max_length=50)
    numero_seguimiento = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)

class DetallePedido(models.Model):
    """Productos dentro de un pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')  # 1:N
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

class Carrito(models.Model):
    """Carrito temporal del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 1:1
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class ItemCarrito(models.Model):
    """Items dentro del carrito"""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')  # 1:N
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ['carrito', 'producto', 'talla']