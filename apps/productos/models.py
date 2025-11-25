from django.db import models
# productos/models.py

class Categoria(models.Model):
    """Tipos de productos: Poleras, Hoodies, Accesorios"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='categorias/')
    activo = models.BooleanField(default=True)
    
class Producto(models.Model):
    """Poleras y productos principales"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # 1:N
    imagen_principal = models.ImageField(upload_to='productos/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)

class Talla(models.Model):
    """Tallas disponibles: XS, S, M, L, XL, XXL"""
    nombre = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=100)
    
class ProductoTalla(models.Model):
    """Relación M:N con stock por talla"""
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['producto', 'talla']

class Etiqueta(models.Model):
    """Tags: punk rock, vintage, calaveras, bandas, etc."""
    nombre = models.CharField(max_length=50, unique=True)
    productos = models.ManyToManyField(Producto, related_name='etiquetas')