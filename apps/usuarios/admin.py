from django.contrib import admin
from apps.usuarios.models import Direccion, Perfil

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('user', 'alias', 'calle', 'numero', 'comuna', 'ciudad', 'region', 'codigo_postal')
    list_filter = ('ciudad', 'region')
    search_fields = ('user__username', 'alias', 'calle', 'ciudad')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'fecha_nacimiento')
    search_fields = ('user__username', 'user__email', 'telefono')
    readonly_fields = ('user',)
