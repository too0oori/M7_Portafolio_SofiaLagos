
from django.views.generic import ListView, DetailView
from apps.productos.models import Producto

class HomeView(ListView):
    """Página principal con productos destacados"""
    model = Producto
    template_name = 'home.html'
    context_object_name = 'productos_destacados'
    
    def get_queryset(self):
        return Producto.objects.filter(activo=True, destacado=True)[:8]

class ProductoListView(ListView):
    """Catálogo completo de productos"""
    model = Producto
    template_name = 'productos/lista.html'
    context_object_name = 'productos'
    paginate_by = 12

class ProductoDetailView(DetailView):
    """Detalle de producto individual"""
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'

class ProductosPorCategoriaView(ListView):
    """Productos filtrados por categoría"""
    model = Producto
    template_name = 'productos/categoria.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        return Producto.objects.filter(
            categoria__pk=self.kwargs['pk'],
            activo=True
        )