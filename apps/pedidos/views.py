from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from apps.productos.models import Producto
from .models import Carrito, ItemCarrito, Pedido, DetallePedido
from django.template import context

@login_required
def agregar_al_carrito(request, producto_id):
    """Lógica personalizada del carrito"""
    producto = get_object_or_404(Producto, pk=producto_id)
    talla_id = request.POST.get('talla')
    cantidad = int(request.POST.get('cantidad', 1))
    
    # Obtener el carrito del usuario
    carrito, created = Carrito.objects.get_or_create(user=request.user)

    # Agregar el producto al carrito
    carrito.items.create(producto=producto, talla=talla_id, cantidad=cantidad)

    # Redirigir al carrito 

    return redirect('carrito')

@login_required
def ver_carrito(request):
    """Vista del carrito"""
    carrito = Carrito.objects.filter(user=request.user).first()

    context = {
        'carrito': carrito
    }
    return render(request, 'pedidos/carrito.html', context)

@login_required
def ver_pedido(request):
    """Vista del pedido"""
    pedido = DetallePedido.objects.filter(user=request.user).first()

    context = {
        'pedido': pedido
    }
    return render(request, 'pedidos/detalle.html')