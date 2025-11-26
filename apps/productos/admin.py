from django.contrib import admin
from django.utils import timezone
from .models import Producto, Categoria, Talla, Etiqueta, ProductoTalla

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'activo', 'destacado')
    list_filter = ('categoria', 'activo', 'destacado', 'fecha_creacion')
    search_fields = ('nombre', 'categoria__nombre')
    readonly_fields = ('fecha_creacion',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.fecha_creacion = timezone.now()
        super().save_model(request, obj, form, change)
    
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'descripcion')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Talla)
class TallaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_productos')
    search_fields = ('nombre',)
    
    def cantidad_productos(self, obj):
        return obj.productos.count()
    cantidad_productos.short_description = 'Cantidad de Productos'

@admin.register(ProductoTalla)
class ProductoTallaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'talla', 'stock')
    list_filter = ('producto', 'talla')
    search_fields = ('producto__nombre', 'talla__nombre')