# FINANZAS MALU

Sistema de gestión de finanzas personales desarrollado con Flask. Permite registrar ingresos y egresos, visualizar estadísticas, crear y seguir metas financieras, programar ahorros, gestionar deudas fijas, y recibir recordatorios automáticos de fechas de pago.

## 🏗️ Arquitectura y Buenas Prácticas

Este proyecto implementa las siguientes buenas prácticas de desarrollo:

- ✅ **Arquitectura MVC** con separación clara de responsabilidades
- ✅ **Capa de Servicios** para lógica de negocio reutilizable
- ✅ **Validación de datos** en backend y frontend
- ✅ **Manejo centralizado de errores**
- ✅ **Configuración por entornos** (Development, Production, Testing)
- ✅ **Pruebas unitarias y de integración** con pytest
- ✅ **Documentación completa** del código y proyecto
- ✅ **Control de versiones** con estructura Git Flow
- ✅ **CI/CD** con GitHub Actions

## Características Principales

### 🔐 Autenticación
- Registro de usuarios
- Inicio de sesión
- Recuperación de contraseña por email
- Sesiones seguras con Flask-Login

### 💰 Gestión de Transacciones
- Registro de ingresos y egresos
- Clasificación por categorías
- Edición y eliminación de transacciones
- Historial completo con paginación

### 📊 Dashboard y Estadísticas
- Vista general de ingresos, egresos y balance del mes
- Gráficos interactivos:
  - Gráfico de líneas: Ingresos vs Egresos (últimos 6 meses)
  - Gráfico de barras: Comparativa mensual
  - Gráfico de pastel: Egresos por categoría
- Resumen de últimas transacciones
- Metas activas y recordatorios pendientes

### 🎯 Metas Financieras
- Crear metas de ahorro con monto objetivo y fecha límite
- Seguimiento de progreso con barras de progreso
- Agregar montos a las metas
- Alertas automáticas cuando las metas están próximas a vencer (30 días)
- Visualización de metas completadas

### 💵 Ahorros Programados
- Crear ahorros con frecuencia configurable:
  - Diaria
  - Semanal
  - Mensual
  - Anual
- Activar/desactivar ahorros
- Fechas de inicio y fin configurables

### 🔔 Recordatorios Automáticos
- Crear recordatorios de pagos pendientes
- Notificaciones automáticas por email
- Tarea programada que verifica recordatorios diariamente a las 9:00 AM
- Seguimiento de recordatorios enviados

### 📡 API REST
API completa para todas las operaciones CRUD:

#### Endpoints disponibles:
- `GET /api/ingresos` - Listar ingresos
- `POST /api/ingresos` - Crear ingreso
- `GET /api/ingresos/<id>` - Obtener ingreso
- `PUT /api/ingresos/<id>` - Actualizar ingreso
- `DELETE /api/ingresos/<id>` - Eliminar ingreso

- `GET /api/egresos` - Listar egresos
- `POST /api/egresos` - Crear egreso
- `GET /api/egresos/<id>` - Obtener egreso
- `PUT /api/egresos/<id>` - Actualizar egreso
- `DELETE /api/egresos/<id>` - Eliminar egreso

- `GET /api/metas` - Listar metas
- `POST /api/metas` - Crear meta
- `PUT /api/metas/<id>` - Actualizar meta
- `DELETE /api/metas/<id>` - Eliminar meta

- `GET /api/ahorros` - Listar ahorros
- `POST /api/ahorros` - Crear ahorro
- `PUT /api/ahorros/<id>` - Actualizar ahorro
- `DELETE /api/ahorros/<id>` - Eliminar ahorro

- `GET /api/recordatorios` - Listar recordatorios
- `POST /api/recordatorios` - Crear recordatorio
- `PUT /api/recordatorios/<id>` - Actualizar recordatorio
- `DELETE /api/recordatorios/<id>` - Eliminar recordatorio

- `GET /api/estadisticas` - Obtener estadísticas del usuario

Todas las rutas de API requieren autenticación.

## Tecnologías Utilizadas

- **Backend**: Flask 3.0.0
- **Base de Datos**: SQLite (configurable para PostgreSQL/MySQL)
- **ORM**: SQLAlchemy
- **Autenticación**: Flask-Login
- **Migraciones**: Flask-Migrate
- **Email**: Flask-Mail
- **Tareas Programadas**: APScheduler
- **Frontend**: Bootstrap 5.3, Chart.js
- **Iconos**: Bootstrap Icons

## Instalación

### 🚀 Instalación Rápida (Windows)

**Opción 1: Instalador Automático**
1. Haz doble clic en `instalar.bat`
2. Espera a que termine la instalación
3. Ejecuta `iniciar.bat` para iniciar la aplicación

**Opción 2: Instalación Manual**

### Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para control de versiones)

### Pasos de Instalación

1. **Navegar al directorio del proyecto**
```bash
cd C:\xampp\htdocs\Finanzas
```

2. **Crear un entorno virtual (OBLIGATORIO)**
```bash
python -m venv venv

# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# En Windows (CMD):
venv\Scripts\activate.bat

# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
- Crea un archivo `.env` (puedes copiar de `.env.example`)
- Configura tus credenciales de email (opcional)

5. **Inicializar base de datos**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

**📖 Para instrucciones detalladas, consulta [INSTALACION.md](INSTALACION.md)**

4. **Configurar variables de entorno**
Crea un archivo `.env` en la raíz del proyecto (puedes copiar `.env.example`):
```env
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DATABASE_URL=sqlite:///finanzas.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
MAIL_DEFAULT_SENDER=tu-email@gmail.com
```

**Nota para Gmail**: Necesitarás generar una "Contraseña de aplicación" en tu cuenta de Google:
1. Ve a tu cuenta de Google
2. Seguridad > Verificación en 2 pasos
3. Contraseñas de aplicaciones
4. Genera una nueva contraseña para "Correo"

5. **Inicializar la base de datos**
```bash
python app.py
```
Esto creará automáticamente las tablas necesarias.

## Uso

### Iniciar la Aplicación

**Windows:**
- Opción 1: Doble clic en `iniciar.bat`
- Opción 2: Desde la terminal:
```bash
# Activar entorno virtual
venv\Scripts\activate

# Iniciar aplicación
python app.py
```

**Linux/Mac:**
```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar aplicación
python app.py
```

2. **Abrir en el navegador**
```
http://localhost:5000
```

3. **Crear tu primera cuenta**
- Haz clic en "Regístrate aquí"
- Completa el formulario
- Inicia sesión con tus credenciales

3. **Crear una cuenta**
- Haz clic en "Regístrate aquí" en la página de inicio de sesión
- Completa el formulario de registro

4. **Comenzar a usar la aplicación**
- Registra tus primeros ingresos y egresos
- Crea metas financieras
- Programa ahorros
- Configura recordatorios de pago

## Estructura del Proyecto

```
Finanzas/
├── app.py                 # Factory de aplicación Flask
├── config.py              # Configuraciones por entorno
├── database.py            # Instancia de SQLAlchemy
├── models.py              # Modelos de datos (User, Ingreso, Egreso, etc.)
├── requirements.txt       # Dependencias del proyecto
├── setup.py               # Configuración del paquete
├── pytest.ini             # Configuración de pytest
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore            # Archivos a ignorar en Git
├── .gitattributes        # Atributos de Git
│
├── routes/               # Controladores (Blueprints)
│   ├── __init__.py
│   ├── auth.py           # Autenticación
│   ├── main.py           # Dashboard
│   ├── transacciones.py  # Ingresos y egresos
│   ├── metas.py          # Metas financieras
│   ├── ahorros.py        # Ahorros programados
│   ├── recordatorios.py  # Recordatorios
│   └── api.py            # API REST
│
├── services/             # Lógica de negocio
│   ├── __init__.py
│   ├── validators.py     # Validadores de datos
│   ├── transacciones_service.py
│   └── metas_service.py
│
├── utils/                 # Utilidades
│   ├── __init__.py
│   └── error_handler.py  # Manejo de errores
│
├── tests/                 # Pruebas
│   ├── __init__.py
│   ├── conftest.py       # Fixtures de pytest
│   ├── test_validators.py
│   ├── test_transacciones_service.py
│   └── test_auth.py
│
└── templates/            # Vistas (Plantillas HTML)
    ├── base.html
    ├── dashboard.html
    ├── auth/
    ├── transacciones/
    ├── metas/
    ├── ahorros/
    └── recordatorios/
```

Ver [ARCHITECTURE.md](ARCHITECTURE.md) para más detalles sobre la arquitectura.

## Características de Seguridad

- Contraseñas hasheadas con Werkzeug
- Protección CSRF (Flask por defecto)
- Autenticación requerida para todas las rutas protegidas
- Validación de datos en formularios
- Tokens seguros para recuperación de contraseña con expiración

## Notificaciones

### Email
- Recordatorios de pago automáticos
- Recuperación de contraseña
- Configuración requerida en `.env`

### Alertas en la App
- Alertas de metas próximas a vencer (30 días)
- Notificaciones de recordatorios pendientes
- Mensajes flash para acciones del usuario

## Personalización

### Cambiar Base de Datos
Para usar PostgreSQL o MySQL, modifica `DATABASE_URL` en `.env`:
```env
# PostgreSQL
DATABASE_URL=postgresql://usuario:contraseña@localhost/finanzas

# MySQL
DATABASE_URL=mysql://usuario:contraseña@localhost/finanzas
```

### Configurar Horario de Recordatorios
En `app.py`, modifica la hora del cron job:
```python
scheduler.add_job(
    func=verificar_recordatorios,
    trigger='cron',
    hour=9,  # Cambiar la hora aquí
    minute=0,
    ...
)
```

## Solución de Problemas

### Error de conexión a email
- Verifica las credenciales en `.env`
- Para Gmail, usa una contraseña de aplicación
- Verifica que el puerto y servidor SMTP sean correctos

### Error de base de datos
- Asegúrate de que SQLite esté instalado (viene con Python)
- Verifica los permisos de escritura en el directorio

### Recordatorios no se envían
- Verifica la configuración de email
- Revisa que el scheduler esté corriendo
- Verifica los logs en la consola

## Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Pruebas

El proyecto incluye pruebas unitarias y de integración usando pytest.

### Ejecutar Pruebas

```bash
# Todas las pruebas
pytest

# Con cobertura
pytest --cov=. --cov-report=html

# Pruebas específicas
pytest tests/test_validators.py

# Con verbose
pytest -v
```

### Cobertura de Código

El objetivo es mantener una cobertura mínima del 80%. Ver reporte en `htmlcov/index.html` después de ejecutar con `--cov-report=html`.

## Desarrollo

### Estructura de Ramas Git

El proyecto sigue Git Flow:

- `main`: Código de producción
- `develop`: Rama de desarrollo
- `feature/*`: Nuevas características
- `bugfix/*`: Corrección de bugs
- `hotfix/*`: Correcciones urgentes

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

### Ejecutar en Modo Desarrollo

```bash
# Configurar entorno
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development       # Windows

# Ejecutar con recarga automática
python app.py
```

### Linting

```bash
# Instalar flake8
pip install flake8

# Ejecutar linting
flake8 .
```

## Documentación

- [README.md](README.md) - Este archivo
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitectura del proyecto
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Documentación de la API
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución

## CI/CD

El proyecto incluye GitHub Actions para:
- Ejecutar pruebas en múltiples versiones de Python
- Verificar linting
- Generar reportes de cobertura

Ver `.github/workflows/ci.yml` para más detalles.

## 📦 Documentación de Entrega

Para información completa sobre la entrega, instalación y despliegue, consulta:

- **[ENTREGA.md](ENTREGA.md)** - Documento completo de entrega con toda la información
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía detallada de despliegue en diferentes entornos

## Soporte

Para reportar problemas o solicitar características, por favor abre un issue en el repositorio del proyecto.

