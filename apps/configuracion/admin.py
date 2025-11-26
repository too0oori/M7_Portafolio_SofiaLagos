from django.contrib import admin

@admin.register
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('nombre_sitio', 'email_contacto', 'telefono', 'costo_envio', 'envio_gratis_desde')
    search_fields = ('nombre_sitio', 'email_contacto', 'telefono')
    readonly_fields = ('nombre_sitio', 'email_contacto', 'telefono', 'costo_envio', 'envio_gratis_desde')
