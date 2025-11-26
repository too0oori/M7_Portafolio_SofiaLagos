#urls de app pedidos

from django.urls import path
from apps.pedidos import views

app_name = 'apps.pedidos'

urlpatterns = [
    path('', views.index, name='index'),
    path('carrito/<int:pk>', views.agregar_al_carrito, name='carrito'),
    path('detalle/<int:pk>', views.ver_carrito, name='detalle'),
    path('pedido/<int:pk>', views.pedido, name='pedido'),
]
