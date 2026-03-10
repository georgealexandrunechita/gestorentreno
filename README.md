# Gestor de Entrenos

Pequeña aplicación en Django para gestionar entrenamientos de un atleta (correr, etc.) como práctica de 2º DAW – Servidor.

## Requisitos

- Python 3.11 (o similar)
- Django 5
- Entorno virtual recomendado [web:270]

## Instalación

```bash
# Crear y activar entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt  # si lo tienes
# o como mínimo
pip install django



Puesta en marcha
bash
python manage.py migrate
python manage.py createsuperuser  # para acceder al admin (opcional)
python manage.py runserver


La aplicación estará disponible en http://127.0.0.1:8000/.

Funcionalidad
Registro y login de usuario usando el sistema de autenticación de Django.

Gestión de perfil de atleta (datos básicos, validaciones de edad y peso).

Creación y listado de entrenamientos (tipo, distancia, duración, notas).

Vistas protegidas que requieren inicio de sesión.

Página de estadísticas básicas de los entrenamientos. 

Tests
El proyecto incluye tests unitarios para modelos y vistas básicas.

Ejecutar tests:
python manage.py test tracker
