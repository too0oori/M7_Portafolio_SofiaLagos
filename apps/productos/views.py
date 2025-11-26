
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from apps.productos.models import Producto, Categoria
from .forms import ProductoForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages


class HomeView(ListView):
    """Página principal con productos destacados"""
    model = Producto
    template_name = 'home.html'
    context_object_name = 'productos_destacados'
    
    def get_queryset(self):
        return Producto.objects.filter(activo=True, destacado=True)[:8]

class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/lista.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        qs = Producto.objects.filter(activo=True)

        categoria_id = self.request.GET.get("categoria")
        if categoria_id:
            qs = qs.filter(categoria_id=categoria_id)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["categoria_actual"] = self.request.GET.get("categoria")
        return context

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'


class CrearProductoView(CreateView):
    model = Producto
    template_name = 'productos/formulario.html'
    form_class = ProductoForm
    success_url = reverse_lazy('apps.productos:lista_productos')

    def form_valid(self, form):
        messages.success(self.request, "Producto creado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el producto.")
        return super().form_invalid(form)

class EliminarProductoView(DeleteView):
    model = Producto
    template_name = 'productos/eliminar.html'
    success_url = reverse_lazy('apps.productos:lista_productos')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Producto eliminado.")
        return super().delete(request, *args, **kwargs)
    
class EditarProductoView(UpdateView):
    model = Producto
    template_name = 'productos/formulario.html'
    form_class = ProductoForm
    success_url = reverse_lazy('apps.productos:lista_productos')

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado correctamente.")
        return super().form_valid(form)
    
def archivo(request):
    return render(request, "productos/archivo.html")