
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from apps.productos.models import Producto, Talla

def agregar_al_carrito(request, pk):
    """
    Agrega un producto al carrito usando sesiones
    """
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=pk)
        carrito = request.session.get("carrito", {})
        
        # Obtener cantidad del formulario
        cantidad = int(request.POST.get('cantidad', 1))
        
        # Obtener talla si existe
        talla_id = request.POST.get('talla')
        
        # Crear clave única (producto + talla si existe)
        if talla_id:
            clave = f"{pk}_{talla_id}"
            talla = get_object_or_404(Talla, pk=talla_id)
            talla_nombre = talla.nombre
        else:
            clave = str(pk)
            talla_nombre = None
        
        # Si el producto ya está, aumentar cantidad
        if clave in carrito:
            carrito[clave]["cantidad"] += cantidad
        else:
            carrito[clave] = {
                "producto_id": pk,
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "cantidad": cantidad,
                "talla": talla_nombre,
                "talla_id": talla_id,
                "imagen": producto.imagen_principal.url if producto.imagen_principal else ""
            }
        
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, f"✓ {producto.nombre} agregado al carrito")
        
        return redirect("apps.productos:detalle_producto", pk=pk)
    
    # Si no es POST, redirigir al detalle
    return redirect("apps.productos:detalle_producto", pk=pk)


def eliminar_item(request, pk):
    """
    Elimina un item específico del carrito
    El pk aquí es la clave del carrito (puede ser "5" o "5_2" si tiene talla)
    """
    carrito = request.session.get("carrito", {})
    
    # Buscar por clave exacta o por producto_id
    clave_encontrada = None
    for clave, item in carrito.items():
        if clave == str(pk) or str(item.get('producto_id')) == str(pk):
            clave_encontrada = clave
            break
    
    if clave_encontrada:
        del carrito[clave_encontrada]
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, "Producto eliminado del carrito")
    
    return redirect("apps.pedidos:ver_carrito")


def ver_carrito(request):
    """
    Muestra el contenido del carrito
    """
    carrito = request.session.get("carrito", {})
    
    total = sum(
        float(item["precio"]) * int(item["cantidad"]) 
        for item in carrito.values()
    )
    
    return render(request, "pedidos/carrito.html", {
        "carrito": carrito,
        "total": total
    })


def vaciar_carrito(request):
    """
    Vacía todo el carrito
    """
    if "carrito" in request.session:
        request.session["carrito"] = {}
        request.session.modified = True
        messages.info(request, "Carrito vaciado")
    
    return redirect("apps.pedidos:ver_carrito")