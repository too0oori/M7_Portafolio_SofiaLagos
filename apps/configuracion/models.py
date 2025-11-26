from django.db import models


class ConfiguracionSitio(models.Model):
    """Configuración global - para requisito de modelo sin relaciones"""
    nombre_sitio = models.CharField(max_length=100, default="A Medias Tintas")
    email_contacto = models.EmailField(default="contacto@amediastintas.cl")
    telefono = models.CharField(max_length=15, default="+56912345678")
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=3000)
    envio_gratis_desde = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    
    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuración del Sitio"
    
    def __str__(self):
        return self.nombre_sitio