import os
import django
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def run_command(cmd):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Éxito")
        return True
    else:
        print(f"✗ Error: {result.stderr}")
        return False

def main():
    print("\n" + "="*60)
    print("IMPORTACIÓN DE BASE DE DATOS")
    print("="*60 + "\n")
    
    export_dir = "database_export"
    
    # Orden de importación (respetando dependencias)
    import_order = [
        # 1. Usuarios primero (no tienen dependencias)
        "auth_user.json",
        
        # 2. Grupos (dependen de users)
        "auth_group.json",
        
        # 3. Tus modelos de negocio (ajusta según tu proyecto)
        "productos_categoria.json",
        "productos_producto.json",
        "carrito_carrito.json",
        "carrito_itemcarrito.json",
        "pedidos_pedido.json",
        "pedidos_itempedido.json",
        
        # Agrega más según los archivos que tengas
    ]
    
    print("1️⃣ Ejecutando migraciones...")
    if not run_command("python manage.py migrate"):
        print("\n❌ Error en migraciones. Deteniendo importación.")
        return
    
    print("\n2️⃣ Cargando datos...")
    success_count = 0
    
    for filename in import_order:
        filepath = os.path.join(export_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⊘ {filename}: No encontrado, saltando...")
            continue
        
        if run_command(f"python manage.py loaddata {filepath}"):
            success_count += 1
    
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print(f"Archivos importados exitosamente: {success_count}/{len(import_order)}")
    print("\n✓ IMPORTACIÓN COMPLETADA")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()