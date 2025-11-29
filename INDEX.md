# 📚 Índice de Documentación - FINANZAS MALU

Este índice te ayudará a navegar por toda la documentación del proyecto.

## 🚀 Inicio Rápido

1. **[ENTREGA.md](ENTREGA.md)** - ⭐ **COMENZAR AQUÍ** - Documento completo de entrega con toda la información
2. **[README.md](README.md)** - Documentación principal del proyecto
3. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía detallada de despliegue

## 📖 Documentación Técnica

### Arquitectura y Diseño
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura del sistema, estructura MVC, flujo de datos
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guía de contribución, estructura de ramas Git

### APIs y Desarrollo
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Documentación completa de la API REST
- **[README.md](README.md)** - Características, instalación básica, uso

### Despliegue
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guías de despliegue:
  - Local
  - Producción con Gunicorn
  - Docker
  - Heroku
  - VPS con Nginx
  - Configuración SSL

## 📁 Estructura del Código

### Backend

#### Aplicación Principal
- `app.py` - Factory de aplicación Flask
- `config.py` - Configuraciones por entorno
- `database.py` - Instancia de SQLAlchemy
- `models.py` - Modelos de datos (ORM)

#### Controladores (Routes)
- `routes/auth.py` - Autenticación, registro, recuperación de contraseña
- `routes/main.py` - Dashboard principal
- `routes/transacciones.py` - Gestión de ingresos y egresos
- `routes/metas.py` - Metas financieras
- `routes/ahorros.py` - Ahorros programados
- `routes/recordatorios.py` - Recordatorios de pago
- `routes/api.py` - API REST completa

#### Servicios (Lógica de Negocio)
- `services/validators.py` - Validadores de datos reutilizables
- `services/transacciones_service.py` - Lógica de transacciones
- `services/metas_service.py` - Lógica de metas

#### Utilidades
- `utils/error_handler.py` - Manejo centralizado de errores

### Frontend

#### Templates (Vistas)
- `templates/base.html` - Template base con navegación
- `templates/dashboard.html` - Dashboard con gráficos
- `templates/auth/` - Páginas de autenticación
- `templates/transacciones/` - Gestión de ingresos/egresos
- `templates/metas/` - Gestión de metas
- `templates/ahorros/` - Gestión de ahorros
- `templates/recordatorios/` - Gestión de recordatorios

### Pruebas
- `tests/conftest.py` - Fixtures de pytest
- `tests/test_validators.py` - Pruebas de validadores
- `tests/test_transacciones_service.py` - Pruebas de servicios
- `tests/test_auth.py` - Pruebas de autenticación

## 🔧 Archivos de Configuración

- `requirements.txt` - Dependencias Python
- `pytest.ini` - Configuración de pytest
- `setup.py` - Configuración del paquete
- `Makefile` - Comandos automatizados
- `.env.example` - Ejemplo de variables de entorno
- `.gitignore` - Archivos ignorados por Git
- `.gitattributes` - Atributos de Git
- `.github/workflows/ci.yml` - CI/CD con GitHub Actions

## 📋 Guías por Tarea

### Para Instalar
1. Lee **[ENTREGA.md](ENTREGA.md)** sección "Instalación y Configuración"
2. O **[README.md](README.md)** sección "Instalación"

### Para Desplegar
1. Lee **[DEPLOYMENT.md](DEPLOYMENT.md)** completo
2. Elige tu método de despliegue preferido

### Para Entender la Arquitectura
1. Lee **[ARCHITECTURE.md](ARCHITECTURE.md)**
2. Revisa el código en `routes/`, `services/`, `models.py`

### Para Usar la API
1. Lee **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**
2. Ejemplos incluidos para cURL, JavaScript, Python

### Para Contribuir
1. Lee **[CONTRIBUTING.md](CONTRIBUTING.md)**
2. Sigue la estructura de ramas Git Flow

### Para Ejecutar Pruebas
1. Lee **[README.md](README.md)** sección "Pruebas"
2. O ejecuta: `pytest` o `make test`

## 🎯 Ruta de Aprendizaje Recomendada

### Principiante
1. **[ENTREGA.md](ENTREGA.md)** - Visión general
2. **[README.md](README.md)** - Instalación y uso básico
3. Explora `templates/` para ver la interfaz

### Intermedio
1. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Entender la estructura
2. Revisa `routes/` y `services/` para ver la separación
3. **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Usar la API

### Avanzado
1. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Desplegar en producción
2. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribuir al proyecto
3. Revisa `tests/` para entender las pruebas

## 📊 Resumen de Características

### Funcionalidades
- ✅ Autenticación completa (registro, login, recuperación)
- ✅ Gestión de ingresos y egresos
- ✅ Metas financieras con seguimiento
- ✅ Ahorros programados con frecuencias
- ✅ Recordatorios automáticos por email
- ✅ Dashboard con gráficos interactivos
- ✅ API REST completa

### Tecnologías
- Backend: Flask, SQLAlchemy, APScheduler
- Frontend: Bootstrap 5, Chart.js, Jinja2
- Testing: pytest, pytest-cov
- CI/CD: GitHub Actions

### Buenas Prácticas
- Arquitectura MVC
- Separación de servicios
- Validación en múltiples capas
- Manejo centralizado de errores
- Pruebas automatizadas
- Documentación completa

## 🆘 ¿Necesitas Ayuda?

1. **Problemas de instalación**: Revisa **[ENTREGA.md](ENTREGA.md)** sección "Solución de Problemas"
2. **Errores de despliegue**: Revisa **[DEPLOYMENT.md](DEPLOYMENT.md)** sección "Troubleshooting"
3. **Preguntas sobre código**: Revisa **[ARCHITECTURE.md](ARCHITECTURE.md)**
4. **Problemas con API**: Revisa **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**

## 📝 Notas Finales

- Todos los archivos están documentados con docstrings
- El código sigue PEP 8
- Las pruebas tienen cobertura > 80%
- La documentación está actualizada

---

**Última actualización:** 2024  
**Versión:** 1.0.0  
**Nombre del Sistema:** FINANZAS MALU

