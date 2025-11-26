#urls.py de productos

from django.urls import path
from . import views

app_name = 'apps.productos'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('categoria/<int:pk>', views.ProductosPorCategoriaView.as_view(), name='categoria'),
    path('producto/<int:pk>', views.ProductoDetailView.as_view(), name='producto'),
]


