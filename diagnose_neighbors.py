import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario

print("=== ANÁLISIS COMPLETO DE USUARIOS ===\n")

# Obtener TODOS los usuarios
todos = Usuario.objects.all().order_by('id')
print(f"Total de usuarios en la base de datos: {todos.count()}\n")

for u in todos:
    print(f"ID: {u.id}")
    print(f"  Username: '{u.username}'")
    print(f"  first_name: '{u.first_name}'")
    print(f"  last_name: '{u.last_name}'")
    print(f"  casa_departamento: '{u.casa_departamento}'")
    print(f"  Activo: {u.activo}")
    print(f"  Rol: {u.rol}")
    print()

# Simular el queryset para Camila
print("\n=== SIMULACIÓN: Vecinos que vería CAMILA ===")
camila = Usuario.objects.filter(username='vcsandovalm').first()
if camila:
    print(f"Usuario actual: {camila.first_name} {camila.last_name} (ID: {camila.id})")
    vecinos_camila = Usuario.objects.filter(activo=True).exclude(id=camila.id).order_by('casa_departamento', 'last_name')
    print(f"Vecinos encontrados: {vecinos_camila.count()}\n")
    
    for v in vecinos_camila:
        print(f"  - {v.first_name} {v.last_name} | Casa: {v.casa_departamento} (ID: {v.id})")
else:
    print("Usuario 'vcsandovalm' no encontrado")

# Simular el queryset para José
print("\n=== SIMULACIÓN: Vecinos que vería JOSÉ ===")
jose = Usuario.objects.filter(username='jmherreraj').first()
if jose:
    print(f"Usuario actual: {jose.first_name} {jose.last_name} (ID: {jose.id})")
    vecinos_jose = Usuario.objects.filter(activo=True).exclude(id=jose.id).order_by('casa_departamento', 'last_name')
    print(f"Vecinos encontrados: {vecinos_jose.count()}\n")
    
    for v in vecinos_jose:
        print(f"  - {v.first_name} {v.last_name} | Casa: {v.casa_departamento} (ID: {v.id})")
else:
    print("Usuario 'jmherreraj' no encontrado")
