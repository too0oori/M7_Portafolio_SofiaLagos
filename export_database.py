import json
import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps
from django.core.serializers import serialize
from django.contrib.contenttypes.models import ContentType

def export_model(model, filename):
    """Exporta un modelo específico a JSON"""
    try:
        queryset = model.objects.all()
        count = queryset.count()
        
        if count == 0:
            print(f"⚠️  {model.__name__}: Sin registros")
            return 0
        
        data = []
        for obj in queryset:
            fields = {}
            for field in model._meta.fields:
                field_name = field.name
                field_value = getattr(obj, field_name)
                
                # Manejar diferentes tipos de campos
                if field_value is None:
                    fields[field_name] = None
                elif hasattr(field_value, 'pk'):  # ForeignKey
                    fields[field_name] = field_value.pk
                elif field.get_internal_type() == 'DateTimeField':
                    fields[field_name] = field_value.isoformat() if field_value else None
                elif field.get_internal_type() == 'DateField':
                    fields[field_name] = field_value.isoformat() if field_value else None
                elif field.get_internal_type() == 'ImageField' or field.get_internal_type() == 'FileField':
                    fields[field_name] = str(field_value) if field_value else ""
                elif field.get_internal_type() == 'DecimalField':
                    fields[field_name] = str(field_value) if field_value else "0"
                else:
                    fields[field_name] = field_value
            
            # Manejar campos ManyToMany
            for m2m in model._meta.many_to_many:
                m2m_values = getattr(obj, m2m.name).all()
                fields[m2m.name] = [m.pk for m in m2m_values]
            
            data.append({
                "model": f"{model._meta.app_label}.{model._meta.model_name}",
                "pk": obj.pk,
                "fields": fields
            })
        
        # Guardar en archivo JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ {model.__name__}: {count} registros → {filename}")
        return count
        
    except Exception as e:
        print(f"✗ Error en {model.__name__}: {str(e)}")
        return 0

def main():
    print("\n" + "="*60)
    print("EXPORTACIÓN COMPLETA DE BASE DE DATOS")
    print("="*60 + "\n")
    
    # Crear carpeta para exports
    export_dir = "database_export"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    total_records = 0
    exported_files = []
    
    # Obtener todas las apps instaladas (excepto las del sistema que no necesitas)
    excluded_apps = [
        'contenttypes', 'sessions', 'admin', 'messages',
        'staticfiles', 'cloudinary', 'cloudinary_storage'
    ]
    
    # Excluir modelos específicos problemáticos
    excluded_models = [
        'auth.permission',
        'auth.group_permissions',
        'auth.user_groups',
        'auth.user_user_permissions',
    ]
    
    for app_config in apps.get_app_configs():
        app_label = app_config.label
        
        if app_label in excluded_apps:
            continue
        
        print(f"\n📦 App: {app_label}")
        print("-" * 60)
        
        for model in app_config.get_models():
            model_name = model._meta.model_name
            model_full_name = f"{app_label}.{model_name}"
            
            # Saltar modelos excluidos
            if model_full_name in excluded_models:
                print(f"⊘ {model.__name__}: Excluido (genera conflictos)")
                continue
            
            filename = os.path.join(export_dir, f"{app_label}_{model_name}.json")
            
            count = export_model(model, filename)
            total_records += count
            
            if count > 0:
                exported_files.append(filename)
    
    # Crear un archivo combinado con todo
    if exported_files:
        print(f"\n" + "="*60)
        print("CREANDO ARCHIVO COMBINADO...")
        print("="*60)
        
        combined_data = []
        for filepath in exported_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined_data.extend(data)
        
        combined_file = os.path.join(export_dir, "database_complete.json")
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Archivo combinado creado: {combined_file}")
    
    # Resumen final
    print(f"\n" + "="*60)
    print("RESUMEN DE EXPORTACIÓN")
    print("="*60)
    print(f"Total de registros exportados: {total_records}")
    print(f"Total de archivos creados: {len(exported_files) + 1}")
    print(f"Carpeta de destino: {export_dir}/")
    print("\nArchivos creados:")
    for filepath in exported_files:
        print(f"  - {os.path.basename(filepath)}")
    print(f"  - database_complete.json (todos combinados)")
    print("\n" + "="*60)
    print("✓ EXPORTACIÓN COMPLETADA")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()