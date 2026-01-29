import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario

print("=== TODOS LOS USUARIOS EN LA BASE DE DATOS ===\n")
usuarios = Usuario.objects.all().order_by('id')

for u in usuarios:
    print(f"ID: {u.id}")
    print(f"  Username: {u.username}")
    print(f"  Nombre completo: {u.first_name} {u.last_name}")
    print(f"  Casa/Dpto: {u.casa_departamento}")
    print(f"  Rol: {u.rol}")
    print(f"  Activo: {u.activo}")
    print(f"  Es superuser: {u.is_superuser}")
    print("-" * 50)

print(f"\nTotal de usuarios: {usuarios.count()}")
