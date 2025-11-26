from django.contrib import admin
from apps.pedidos.models import Pedido, DetallePedido, Carrito, ItemCarrito

#Inline para ver detalles dentro del pedido
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('subtotal',)
    fields = ('producto', 'talla', 'cantidad', 'precio_unitario', 'subtotal')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'total')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('cliente__username', 'cliente__email')
    readonly_fields = ('fecha_pedido', 'total')
    inlines = [DetallePedidoInline]
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('cliente', 'fecha_pedido', 'estado', 'total')
        }),
        ('Envío', {
            'fields': ('direccion_envio', 'direccion_completa', 'numero_seguimiento')
        }),
        ('Pago y Notas', {
            'fields': ('metodo_pago', 'notas')
        }),
    )

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal', 'talla')
    list_filter = ('pedido', 'producto', 'talla')
    search_fields = ('pedido__cliente__username', 'producto__nombre')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('user', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('user__username', 'user__email')

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'talla', 'cantidad')
    list_filter = ('carrito', 'producto', 'talla')