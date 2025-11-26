# usuarios/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Perfil
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.PerfilUpdateView.as_view(), name='editar_perfil'),
    
    # Direcciones
    path('direcciones/agregar/', views.agregar_direccion_view, name='agregar_direccion'),
    path('direcciones/<int:pk>/editar/', views.editar_direccion_view, name='editar_direccion'),
    path('direcciones/<int:pk>/eliminar/', views.eliminar_direccion_view, name='eliminar_direccion'),
]