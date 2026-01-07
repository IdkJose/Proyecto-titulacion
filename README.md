# Sistema de Comunicación Conjunto Selva Alegre

Sistema web para mejorar la comunicación entre vecinos y administración del conjunto habitacional "Selva Alegre".

## Tecnologías
- Django 6.0.1
- Python 3.14.2
- SQLite (base de datos)
- Bootstrap (frontend)
- HTML5, CSS, JavaScript

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Proyecto-titulacion
git checkout backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
**Windows PowerShell:**
```bash
.\venv\Scripts\Activate
```

**Windows CMD:**
```bash
venv\Scripts\activate.bat
```

**Si tienes problemas con PowerShell:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Aplicar migraciones
```bash
python manage.py migrate
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Correr el servidor
```bash
python manage.py runserver
```

Visitar: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## Estructura del Proyecto
```
Proyecto-titulacion/
├── config/          # Configuración principal del proyecto Django
├── venv/            # Entorno virtual (no se sube a git)
├── db.sqlite3       # Base de datos SQLite (no se sube a git)
├── manage.py        # Archivo de comandos de Django
├── requirements.txt # Dependencias del proyecto
├── .gitignore       # Archivos ignorados por git
└── README.md        # Este archivo
```

## Comandos Útiles de Django
```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# Crear migraciones después de modificar modelos
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate

# Crear usuario administrador
python manage.py createsuperuser

# Crear nueva aplicación
python manage.py startapp <nombre_app>

# Abrir shell de Django
python manage.py shell
```

## Funcionalidades del Sistema

### Objetivos del Proyecto
1. **Calendario Informativo**: Facilitar el acceso a fechas y detalles sobre actividades y gestiones del conjunto
2. **Blog Comunitario**: Compartir noticias, actividades y avisos relevantes
3. **Módulo de Reportería**: Generar transparencia documentando las acciones de la junta administrativa

### Módulos Planificados
- 👥 **Usuarios**: Gestión de residentes y administrador
- 📰 **Blog/Comunicación**: Noticias y avisos para la comunidad
- 📅 **Eventos**: Calendario de mingas y actividades
- 📊 **Reportes**: Transparencia de obras y gestión administrativa

## Notas Importantes
- El archivo `venv/` y `db.sqlite3` NO se suben a git
- Cada desarrollador debe crear su propio entorno virtual
- Cada desarrollador debe ejecutar las migraciones localmente
- Mantener `requirements.txt` actualizado cuando se instalen nuevas dependencias

## Contribución
Este es un proyecto de titulación para el conjunto habitacional "Selva Alegre"
