#urls.py de productos

from django.urls import path
from . import views

app_name = 'apps.productos'

urlpatterns = [
    # Listado y detalle
    path('', views.ProductoListView.as_view(), name='lista'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.ProductoDetailView.as_view(), name='detalle_producto'),
    
    # CRUD Administrativo
    path('crear/', views.CrearProductoView.as_view(), name='crear_producto'),
    path('<int:pk>/editar/', views.EditarProductoView.as_view(), name='editar_producto'),
    path('<int:pk>/eliminar/', views.EliminarProductoView.as_view(), name='eliminar_producto'),
    
    # Archivo
    path('archivo/', views.archivo, name='archivo'),
]