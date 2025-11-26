from django.db import models

class Categoria(models.Model):
    """Tipos de productos: Poleras, Hoodies, Accesorios"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='categorias/')
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    """Poleras y productos principales"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen_principal = models.ImageField(upload_to='productos/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.nombre

class Talla(models.Model):
    """Tallas disponibles: XS, S, M, L, XL, XXL"""
    nombre = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Talla"
        verbose_name_plural = "Tallas"
    
    def __str__(self):
        return self.nombre
    
class ProductoTalla(models.Model):
    """Relación M:N con stock por talla"""
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['producto', 'talla']
        verbose_name = "Stock por Talla"
        verbose_name_plural = "Stock por Tallas"
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.talla.nombre} (Stock: {self.stock})"

class Etiqueta(models.Model):
    """Tags: punk rock, vintage, calaveras, bandas, etc."""
    nombre = models.CharField(max_length=50, unique=True)
    productos = models.ManyToManyField(Producto, related_name='etiquetas')
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
    
    def __str__(self):
        return self.nombre