import os
import django
from decouple import config  # Si usas .env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import cloudinary
import cloudinary.uploader
from apps.productos.models import Producto, Categoria

# Configurar Cloudinary
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET')
)

def migrate_images():
    print("Migrando imágenes a Cloudinary...\n")
    
    migrated = 0
    errors = 0
    
    # Migrar imágenes de productos
    productos = Producto.objects.filter(imagen_principal__isnull=False).exclude(imagen_principal='')
    print(f"📦 Encontrados {productos.count()} productos con imágenes\n")
    
    for producto in productos:
        if producto.imagen_principal and hasattr(producto.imagen_principal, 'path'):
            try:
                # Verificar que el archivo existe
                if not os.path.exists(producto.imagen_principal.path):
                    print(f"⚠️  {producto.nombre}: Archivo no encontrado en {producto.imagen_principal.path}")
                    continue
                
                # Subir a Cloudinary
                result = cloudinary.uploader.upload(
                    producto.imagen_principal.path,
                    folder="productos",
                    public_id=f"producto_{producto.id}",
                    overwrite=True,
                    resource_type="image"
                )
                
                # Guardar la URL de Cloudinary
                old_path = producto.imagen_principal.name
                producto.imagen_principal = result['secure_url']
                producto.save()
                
                print(f"✓ {producto.nombre}")
                print(f"  Desde: {old_path}")
                print(f"  Hacia: {result['secure_url']}\n")
                migrated += 1
                
            except Exception as e:
                print(f"✗ Error en {producto.nombre}: {e}\n")
                errors += 1
    
    # Migrar imágenes de categorías
    categorias = Categoria.objects.filter(imagen__isnull=False).exclude(imagen='')
    print(f"\n📂 Encontradas {categorias.count()} categorías con imágenes\n")
    
    for categoria in categorias:
        if categoria.imagen and hasattr(categoria.imagen, 'path'):
            try:
                if not os.path.exists(categoria.imagen.path):
                    print(f"⚠️  {categoria.nombre}: Archivo no encontrado")
                    continue
                
                result = cloudinary.uploader.upload(
                    categoria.imagen.path,
                    folder="categorias",
                    public_id=f"categoria_{categoria.id}",
                    overwrite=True,
                    resource_type="image"
                )
                
                categoria.imagen = result['secure_url']
                categoria.save()
                
                print(f"✓ {categoria.nombre}: {result['secure_url']}\n")
                migrated += 1
                
            except Exception as e:
                print(f"✗ Error en {categoria.nombre}: {e}\n")
                errors += 1
    
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print(f"✓ Imágenes migradas: {migrated}")
    print(f"✗ Errores: {errors}")
    print("="*60 + "\n")

if __name__ == "__main__":
    # Verificar credenciales antes de empezar
    try:
        cloud_name = config('CLOUDINARY_CLOUD_NAME')
        api_key = config('CLOUDINARY_API_KEY')
        api_secret = config('CLOUDINARY_API_SECRET')
        
        print(f"Cloud Name: {cloud_name}")
        print(f"API Key: {api_key[:10]}...")
        print("✓ Credenciales cargadas correctamente\n")
        
        migrate_images()
    except Exception as e:
        print(f"\n❌ Error al cargar credenciales de Cloudinary:")
        print(f"   {e}")
        print("\nAsegúrate de:")
        print("1. Crear un archivo .env con tus credenciales")
        print("2. Instalar python-decouple: pip install python-decouple")
        print("3. Obtener credenciales desde: https://cloudinary.com/console\n")