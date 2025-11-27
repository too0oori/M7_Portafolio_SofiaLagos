
"""
Aqui hay consultas ORM de ejemplo para demostrar diferentes capacidades de Django.
Estas consultas no se usan en producción pero documentan el aprendizaje del ORM segun requerimientos de la tarea
"""

from django.db.models import Count, Avg, Q, F
from .models import Producto, Categoria, Etiqueta

# consultas de agregacion q no ocupé en views
def estadisticas_categoria(categoria_id):
    """
    Calcula precio promedio y total de productos de una categoría.
    Uso: stats = estadisticas_categoria(1)
    """
    return Producto.objects.filter(categoria_id=categoria_id).aggregate(
        promedio=Avg('precio'),
        total_productos=Count('id')
    )


# consultas con q objects

def buscar_productos_avanzado(termino):
    """
    Busca productos por nombre O descripción (búsqueda flexible).
    Uso: productos = buscar_productos_avanzado("evangelion")
    """
    return Producto.objects.filter(
        Q(nombre__icontains=termino) | Q(descripcion__icontains=termino),
        activo=True
    )


#consultas con anotaciones
def categorias_populares():
    """
    Lista categorías ordenadas por cantidad de productos activos.
    Uso: cats = categorias_populares()
    """
    return Categoria.objects.annotate(
        num_productos=Count('producto', filter=Q(producto__activo=True))
    ).filter(num_productos__gt=0).order_by('-num_productos')


#APARTE: Las consultas usadas en producción están en:
#productos/views.py: filter(), get_object_or_404(), relaciones M:N
#pedidos/views.py: operaciones CRUD con sesiones
