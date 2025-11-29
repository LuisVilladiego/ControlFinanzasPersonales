# 📦 Documento de Entrega - FINANZAS MALU

## 📋 Contenido de la Entrega

Este documento contiene toda la información necesaria para entender, instalar, configurar y desplegar el sistema de gestión de finanzas personales FINANZAS MALU.

---

## 📁 Estructura Completa del Proyecto

```
Finanzas/
│
├── 📄 ARCHITECTURE.md          # Documentación de arquitectura
├── 📄 API_DOCUMENTATION.md     # Documentación completa de la API REST
├── 📄 CONTRIBUTING.md          # Guía de contribución
├── 📄 ENTREGA.md              # Este documento
├── 📄 README.md               # Documentación principal
├── 📄 Makefile                # Comandos automatizados
├── 📄 setup.py                # Configuración del paquete Python
├── 📄 pytest.ini              # Configuración de pytest
├── 📄 .gitignore             # Archivos ignorados por Git
├── 📄 .gitattributes         # Atributos de Git
├── 📄 .env.example           # Ejemplo de variables de entorno
│
├── 🔧 app.py                  # Factory de aplicación Flask
├── 🔧 config.py               # Configuraciones por entorno
├── 🔧 database.py             # Instancia de SQLAlchemy
├── 🔧 models.py               # Modelos de datos (ORM)
│
├── 📂 routes/                 # Controladores (Blueprints)
│   ├── __init__.py
│   ├── auth.py               # Autenticación y registro
│   ├── main.py               # Dashboard principal
│   ├── transacciones.py      # Ingresos y egresos
│   ├── metas.py              # Metas financieras
│   ├── ahorros.py            # Ahorros programados
│   ├── recordatorios.py      # Recordatorios de pago
│   └── api.py                # API REST
│
├── 📂 services/               # Lógica de negocio
│   ├── __init__.py
│   ├── validators.py         # Validadores de datos
│   ├── transacciones_service.py  # Servicio de transacciones
│   └── metas_service.py      # Servicio de metas
│
├── 📂 utils/                  # Utilidades
│   ├── __init__.py
│   └── error_handler.py      # Manejo centralizado de errores
│
├── 📂 templates/              # Vistas (Plantillas HTML)
│   ├── base.html             # Template base
│   ├── dashboard.html        # Dashboard principal
│   ├── auth/
│   │   ├── login.html
│   │   ├── registro.html
│   │   ├── recuperar_contraseña.html
│   │   └── resetear_contraseña.html
│   ├── transacciones/
│   │   ├── ingresos.html
│   │   ├── egresos.html
│   │   ├── nuevo_ingreso.html
│   │   ├── nuevo_egreso.html
│   │   ├── editar_ingreso.html
│   │   └── editar_egreso.html
│   ├── metas/
│   │   ├── listar.html
│   │   ├── nueva.html
│   │   ├── ver.html
│   │   └── editar.html
│   ├── ahorros/
│   │   ├── listar.html
│   │   ├── nuevo.html
│   │   └── editar.html
│   └── recordatorios/
│       ├── listar.html
│       ├── nuevo.html
│       └── editar.html
│
├── 📂 tests/                  # Pruebas automatizadas
│   ├── __init__.py
│   ├── conftest.py           # Fixtures de pytest
│   ├── test_validators.py    # Pruebas de validadores
│   ├── test_transacciones_service.py  # Pruebas de servicios
│   └── test_auth.py          # Pruebas de autenticación
│
└── 📂 .github/
    └── workflows/
        └── ci.yml            # GitHub Actions CI/CD
```

---

## 🏗️ Arquitectura del Sistema

### Modelo MVC con Capa de Servicios

El proyecto sigue una arquitectura **MVC (Model-View-Controller)** mejorada con una capa de servicios:

```
┌─────────────────────────────────────┐
│     VISTAS (Templates/HTML)         │
│   Bootstrap 5 + Chart.js + Jinja2   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   CONTROLADORES (Routes/Blueprints) │
│         Flask Blueprints            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    SERVICIOS (Business Logic)       │
│   Validación + Lógica de Negocio    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     MODELOS (Database/ORM)          │
│         SQLAlchemy ORM              │
└─────────────────────────────────────┘
```

### Separación de Responsabilidades

1. **Vistas (Templates)**: Solo presentación, sin lógica
2. **Controladores (Routes)**: Manejan HTTP, validan autenticación, llaman servicios
3. **Servicios**: Contienen toda la lógica de negocio y validaciones
4. **Modelos**: Solo estructura de datos y relaciones

---

## 📚 Librerías y Tecnologías Utilizadas

### Backend

| Librería | Versión | Propósito |
|----------|---------|-----------|
| **Flask** | 3.0.0 | Framework web principal |
| **Flask-SQLAlchemy** | 3.1.1 | ORM para base de datos |
| **Flask-Login** | 0.6.3 | Manejo de sesiones y autenticación |
| **Flask-Mail** | 0.10.0 | Envío de emails |
| **Flask-Migrate** | 4.0.5 | Migraciones de base de datos |
| **Werkzeug** | 3.0.1 | Utilidades WSGI y seguridad |
| **APScheduler** | 3.10.4 | Tareas programadas (recordatorios) |
| **python-dotenv** | 1.0.0 | Manejo de variables de entorno |
| **email-validator** | 2.1.0 | Validación de emails |

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Bootstrap** | 5.3.0 | Framework CSS responsivo |
| **Bootstrap Icons** | 1.10.0 | Iconos |
| **Chart.js** | 4.4.0 | Gráficos interactivos |
| **Jinja2** | (incluido en Flask) | Motor de plantillas |

### Testing y Desarrollo

| Librería | Versión | Propósito |
|----------|---------|-----------|
| **pytest** | 7.4.3 | Framework de pruebas |
| **pytest-cov** | 4.1.0 | Cobertura de código |
| **pytest-flask** | 1.3.0 | Extensiones Flask para pytest |

### Base de Datos

- **SQLite** (por defecto) - Base de datos embebida
- Soporte para **PostgreSQL** y **MySQL** (configurable)

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python 3.9 o superior**
- **pip** (gestor de paquetes)
- **Git** (para clonar el repositorio)
- **Navegador web moderno**

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Finanzas.git
cd Finanzas
```

### Paso 2: Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

O usando Make:
```bash
make install
```

### Paso 4: Configurar Variables de Entorno

1. Copiar el archivo de ejemplo:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

2. Editar `.env` con tus configuraciones:

```env
# Clave secreta (genera una nueva para producción)
SECRET_KEY=tu-clave-secreta-muy-segura-aqui

# Base de datos (SQLite por defecto)
DATABASE_URL=sqlite:///finanzas.db

# Para PostgreSQL:
# DATABASE_URL=postgresql://usuario:contraseña@localhost/finanzas

# Para MySQL:
# DATABASE_URL=mysql://usuario:contraseña@localhost/finanzas

# Configuración de Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
MAIL_DEFAULT_SENDER=tu-email@gmail.com

# Configuración del Scheduler (opcional)
SCHEDULER_TIMEZONE=UTC
SCHEDULER_HOUR=9
SCHEDULER_MINUTE=0

# Configuración de paginación (opcional)
ITEMS_PER_PAGE=10
```

**⚠️ Importante para Gmail:**
1. Activa la verificación en 2 pasos
2. Genera una "Contraseña de aplicación" en tu cuenta de Google
3. Usa esa contraseña en `MAIL_PASSWORD`

### Paso 5: Inicializar Base de Datos

```bash
python app.py
```

Esto creará automáticamente todas las tablas necesarias.

### Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

O usando Make:
```bash
make run
```

La aplicación estará disponible en: **http://localhost:5000**

---

## 🧪 Pruebas

### Ejecutar Todas las Pruebas

```bash
pytest
```

### Con Cobertura

```bash
pytest --cov=. --cov-report=html
```

Luego abre `htmlcov/index.html` en tu navegador para ver el reporte.

### Pruebas Específicas

```bash
# Solo validadores
pytest tests/test_validators.py

# Solo servicios
pytest tests/test_transacciones_service.py

# Solo autenticación
pytest tests/test_auth.py
```

### Usando Make

```bash
make test
```

---

## 📖 Uso de la Aplicación

### 1. Registro de Usuario

1. Abre http://localhost:5000
2. Haz clic en "Regístrate aquí"
3. Completa el formulario:
   - Nombre completo
   - Email
   - Contraseña (mínimo 6 caracteres)
   - Confirmar contraseña

### 2. Iniciar Sesión

1. Ingresa tu email y contraseña
2. Serás redirigido al dashboard

### 3. Registrar Transacciones

**Ingresos:**
- Ve a "Ingresos" en el menú
- Haz clic en "Nuevo Ingreso"
- Completa: monto, descripción, categoría, fecha

**Egresos:**
- Similar proceso en "Egresos"

### 4. Crear Metas Financieras

1. Ve a "Metas" en el menú
2. Haz clic en "Nueva Meta"
3. Define: título, monto objetivo, fecha límite
4. Agrega montos progresivamente desde la vista de la meta

### 5. Programar Ahorros

1. Ve a "Ahorros" en el menú
2. Crea un nuevo ahorro con frecuencia configurable
3. Activa/desactiva según necesites

### 6. Configurar Recordatorios

1. Ve a "Recordatorios"
2. Crea recordatorios de pagos pendientes
3. Recibirás emails automáticos en la fecha configurada

---

## 🌐 Despliegue

### Opción 1: Despliegue Local (Desarrollo)

Ya está configurado. Solo ejecuta:
```bash
python app.py
```

### Opción 2: Despliegue en Producción

#### Usando Gunicorn (Recomendado)

1. Instalar Gunicorn:
```bash
pip install gunicorn
```

2. Configurar variables de entorno:
```bash
export FLASK_ENV=production
export SECRET_KEY=tu-clave-super-segura
```

3. Ejecutar:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Usando Docker (Opcional)

Crear `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Despliegue en Heroku

1. Instalar Heroku CLI
2. Crear `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

3. Desplegar:
```bash
heroku create tu-app-finanzas
git push heroku main
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

#### Despliegue en VPS (Ubuntu/Debian)

1. Instalar dependencias del sistema:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

2. Configurar Nginx como reverse proxy
3. Usar systemd para gestionar el servicio
4. Configurar SSL con Let's Encrypt

---

## 🔧 Configuración Avanzada

### Cambiar Base de Datos

**PostgreSQL:**
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost/finanzas
```

**MySQL:**
```env
DATABASE_URL=mysql://usuario:contraseña@localhost/finanzas
```

Luego ejecutar migraciones:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Configurar Horario de Recordatorios

Edita `.env`:
```env
SCHEDULER_HOUR=9      # Hora (0-23)
SCHEDULER_MINUTE=0    # Minuto (0-59)
SCHEDULER_TIMEZONE=UTC
```

### Modo Debug

Solo en desarrollo:
```env
FLASK_ENV=development
```

---

## 📊 Modelos de Datos

### Esquema de Base de Datos

```
users
├── id (PK)
├── nombre
├── email (UNIQUE)
├── password_hash
└── fecha_registro

ingresos
├── id (PK)
├── usuario_id (FK -> users)
├── monto
├── descripcion
├── categoria
├── fecha
└── fecha_creacion

egresos
├── id (PK)
├── usuario_id (FK -> users)
├── monto
├── descripcion
├── categoria
├── fecha
└── fecha_creacion

metas
├── id (PK)
├── usuario_id (FK -> users)
├── titulo
├── descripcion
├── monto_objetivo
├── monto_actual
├── fecha_limite
├── completada
└── fecha_creacion

ahorros
├── id (PK)
├── usuario_id (FK -> users)
├── titulo
├── descripcion
├── monto
├── frecuencia
├── fecha_inicio
├── fecha_fin
├── activo
└── fecha_creacion

recordatorios
├── id (PK)
├── usuario_id (FK -> users)
├── titulo
├── descripcion
├── monto
├── fecha_pago
├── fecha_recordatorio
├── enviado
└── fecha_creacion

tokens_recuperacion
├── id (PK)
├── usuario_id (FK -> users)
├── token (UNIQUE)
├── fecha_expiracion
├── usado
└── fecha_creacion
```

---

## 🔐 Seguridad

### Implementado

- ✅ Contraseñas hasheadas con Werkzeug
- ✅ Protección CSRF (Flask por defecto)
- ✅ Autenticación requerida para rutas protegidas
- ✅ Validación de datos en backend
- ✅ Tokens seguros para recuperación de contraseña
- ✅ Expiración de tokens (24 horas)
- ✅ Sanitización de inputs

### Recomendaciones para Producción

1. **Cambiar SECRET_KEY**: Genera una clave segura
2. **Usar HTTPS**: Configurar SSL/TLS
3. **Rate Limiting**: Implementar límites de requests
4. **Logging**: Configurar logs de seguridad
5. **Backup**: Realizar backups regulares de la BD

---

## 📝 API REST

La aplicación incluye una API REST completa. Ver [API_DOCUMENTATION.md](API_DOCUMENTATION.md) para documentación detallada.

**Endpoints principales:**
- `GET/POST /api/ingresos`
- `GET/POST /api/egresos`
- `GET/POST /api/metas`
- `GET/POST /api/ahorros`
- `GET/POST /api/recordatorios`
- `GET /api/estadisticas`

Todas las rutas requieren autenticación mediante sesión.

---

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"

**Solución:** Activa el entorno virtual y reinstala dependencias:
```bash
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

### Error: "Database is locked" (SQLite)

**Solución:** Cierra otras conexiones a la base de datos o usa PostgreSQL/MySQL.

### Recordatorios no se envían

**Solución:**
1. Verifica configuración de email en `.env`
2. Para Gmail, usa contraseña de aplicación
3. Revisa logs de la aplicación

### Error de importación circular

**Solución:** Ya está resuelto usando `database.py` separado.

---

## 📚 Documentación Adicional

- **[README.md](README.md)** - Documentación principal
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura detallada
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Documentación de API
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guía de contribución

---

## ✅ Checklist de Entrega

- [x] Código backend completo (Flask, modelos, servicios)
- [x] Código frontend completo (Templates HTML, CSS, JS)
- [x] Rutas y controladores implementados
- [x] Modelos de base de datos
- [x] Validación de datos (backend y frontend)
- [x] Manejo de errores
- [x] Pruebas unitarias y de integración
- [x] Documentación completa
- [x] Instrucciones de instalación
- [x] Configuración de despliegue
- [x] Arquitectura documentada
- [x] Librerías documentadas

---

## 📞 Soporte

Para problemas o preguntas:
1. Revisa la documentación
2. Consulta los issues en GitHub
3. Abre un nuevo issue si es necesario

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

---

**Versión:** 1.0.0  
**Fecha de Entrega:** 2024  
**Nombre del Sistema:** FINANZAS MALU  
**Desarrollado con:** Flask, Python, Bootstrap, Chart.js

