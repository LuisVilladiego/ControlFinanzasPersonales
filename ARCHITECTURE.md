# Arquitectura del Proyecto

Este documento describe la arquitectura y estructura del proyecto FINANZAS MALU.

## Arquitectura General

El proyecto sigue una arquitectura **MVC (Model-View-Controller)** con una capa de servicios adicional:

```
┌─────────────────────────────────────────┐
│           Vistas (Templates)            │
│         (HTML + Bootstrap)               │
└─────────────────┬─────────────────────────┘
                  │
┌─────────────────▼─────────────────────────┐
│         Controladores (Routes)            │
│      (Flask Blueprints)                   │
└─────────────────┬─────────────────────────┘
                  │
┌─────────────────▼─────────────────────────┐
│          Servicios (Business Logic)       │
│    (services/transacciones_service.py)   │
└─────────────────┬─────────────────────────┘
                  │
┌─────────────────▼─────────────────────────┐
│         Modelos (Database)                │
│      (SQLAlchemy ORM)                     │
└───────────────────────────────────────────┘
```

## Estructura de Directorios

```
Finanzas/
├── app.py                 # Factory de aplicación Flask
├── config.py              # Configuraciones
├── database.py            # Instancia de SQLAlchemy
├── models.py              # Modelos de datos
│
├── routes/                # Controladores (Blueprints)
│   ├── auth.py
│   ├── main.py
│   ├── transacciones.py
│   ├── metas.py
│   ├── ahorros.py
│   ├── recordatorios.py
│   └── api.py
│
├── services/              # Lógica de negocio
│   ├── validators.py
│   ├── transacciones_service.py
│   └── metas_service.py
│
├── templates/             # Vistas (HTML)
│   ├── base.html
│   ├── dashboard.html
│   └── [módulos]/
│
├── utils/                 # Utilidades
│   └── error_handler.py
│
├── tests/                 # Pruebas
│   ├── conftest.py
│   ├── test_validators.py
│   ├── test_transacciones_service.py
│   └── test_auth.py
│
└── static/                # Archivos estáticos (opcional)
```

## Capas de la Aplicación

### 1. Capa de Vistas (Templates)

- **Responsabilidad**: Presentación de datos al usuario
- **Tecnologías**: Jinja2, Bootstrap 5, Chart.js
- **Ubicación**: `templates/`

### 2. Capa de Controladores (Routes)

- **Responsabilidad**: Manejar requests HTTP, validar permisos, llamar a servicios
- **Tecnologías**: Flask Blueprints
- **Ubicación**: `routes/`
- **Principios**:
  - Delgados (thin controllers)
  - Solo manejan HTTP
  - Delegan lógica a servicios

### 3. Capa de Servicios

- **Responsabilidad**: Lógica de negocio, validaciones, operaciones complejas
- **Ubicación**: `services/`
- **Principios**:
  - Reutilizables
  - Independientes de Flask
  - Fáciles de testear

### 4. Capa de Modelos

- **Responsabilidad**: Representación de datos, relaciones de BD
- **Tecnologías**: SQLAlchemy ORM
- **Ubicación**: `models.py`
- **Principios**:
  - Solo estructura de datos
  - Sin lógica de negocio
  - Relaciones bien definidas

## Flujo de Datos

### Ejemplo: Crear un Ingreso

1. **Usuario** → Envía formulario HTML
2. **Route** (`routes/transacciones.py`) → Recibe request, valida autenticación
3. **Service** (`services/transacciones_service.py`) → Valida datos, crea ingreso
4. **Model** (`models.py`) → Persiste en BD
5. **Response** → Redirige a lista de ingresos

## Separación de Responsabilidades

### Routes (Controladores)
- ✅ Validar autenticación
- ✅ Extraer datos del request
- ✅ Llamar a servicios
- ✅ Formatear respuesta
- ❌ Lógica de negocio
- ❌ Validaciones complejas
- ❌ Acceso directo a BD

### Services (Lógica de Negocio)
- ✅ Validar datos
- ✅ Lógica de negocio
- ✅ Operaciones complejas
- ✅ Transacciones de BD
- ❌ Manejo de HTTP
- ❌ Renderizado de templates

### Models (Datos)
- ✅ Estructura de datos
- ✅ Relaciones
- ✅ Métodos de acceso
- ❌ Lógica de negocio
- ❌ Validaciones

## Validación de Datos

La validación se realiza en dos niveles:

1. **Frontend**: Validación básica en formularios HTML
2. **Backend**: Validación completa en `services/validators.py`

## Manejo de Errores

- **Centralizado**: `utils/error_handler.py`
- **Decoradores**: `@handle_errors`, `@handle_api_errors`
- **Logging**: Flask logger para errores

## Configuración

- **Archivo**: `config.py`
- **Entornos**: Development, Production, Testing
- **Variables**: `.env` (no versionado)

## Pruebas

- **Framework**: pytest
- **Cobertura**: pytest-cov
- **Tipos**:
  - Unitarias: Servicios, validadores
  - Integración: Rutas, API
  - Fixtures: `tests/conftest.py`

## Mejores Prácticas Implementadas

1. ✅ Separación de responsabilidades
2. ✅ Código DRY (Don't Repeat Yourself)
3. ✅ Validación en múltiples capas
4. ✅ Manejo centralizado de errores
5. ✅ Configuración por entornos
6. ✅ Pruebas automatizadas
7. ✅ Documentación en código
8. ✅ Type hints donde es posible

## Extensiones Futuras

- Repositorios para abstracción de BD
- DTOs (Data Transfer Objects)
- Eventos y handlers
- Caché para consultas frecuentes
- Logging estructurado

