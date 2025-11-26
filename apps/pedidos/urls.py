#urls de app pedidos

from django.urls import path
from apps.pedidos import views

app_name = 'apps.pedidos'

urlpatterns = [
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar'),
    path('ver/', views.ver_carrito, name='ver'),
]
