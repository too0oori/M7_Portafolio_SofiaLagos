from django.urls import path
from apps.pedidos import views

app_name = 'apps.pedidos'

urlpatterns = [
    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:pk>/', views.agregar_al_carrito, name='agregar_carrito'),
    path('carrito/eliminar/<int:pk>/', views.eliminar_item, name='eliminar_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
]