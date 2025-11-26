#urls.py de productos

from django.urls import path
from . import views

app_name = 'apps.productos'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('catalogo/', views.ProductoListView.as_view(), name='lista'),
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(), name='detalle_producto'),
    path('crear/', views.CrearProductoView.as_view(), name='crear'),
    path('editar/<int:pk>', views.EditarProductoView.as_view(), name='editar'),
    path('eliminar/<int:pk>', views.EliminarProductoView.as_view(), name='eliminar'),
    path("archivo/", views.archivo, name="archivo"),
]


