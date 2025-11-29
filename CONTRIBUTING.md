# Guía de Contribución

Gracias por tu interés en contribuir a este proyecto. Esta guía te ayudará a entender cómo contribuir de manera efectiva.

## Estructura de Ramas

El proyecto sigue una estructura de ramas Git Flow:

- **main/master**: Rama principal de producción. Solo código estable y probado.
- **develop**: Rama de desarrollo. Integración de nuevas características.
- **feature/**: Ramas para nuevas características (ej: `feature/nueva-funcionalidad`)
- **bugfix/**: Ramas para corrección de bugs (ej: `bugfix/corregir-error`)
- **hotfix/**: Ramas para correcciones urgentes en producción (ej: `hotfix/error-critico`)
- **release/**: Ramas para preparar releases (ej: `release/v1.1.0`)

## Proceso de Contribución

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/tu-usuario/Finanzas.git
cd Finanzas
```

### 2. Crear una Rama

```bash
# Asegúrate de estar en develop
git checkout develop
git pull origin develop

# Crea una nueva rama para tu feature
git checkout -b feature/mi-nueva-funcionalidad
```

### 3. Desarrollo

- Sigue las convenciones de código del proyecto
- Escribe código limpio y bien documentado
- Agrega pruebas para nuevas funcionalidades
- Asegúrate de que todas las pruebas pasen

### 4. Commits

Usa mensajes de commit descriptivos siguiendo el formato:

```
tipo(alcance): descripción breve

Descripción más detallada si es necesario
```

Tipos:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (no afectan código)
- `refactor`: Refactorización de código
- `test`: Agregar o modificar pruebas
- `chore`: Tareas de mantenimiento

Ejemplo:
```
feat(transacciones): agregar validación de montos negativos

Se agregó validación para prevenir ingresos/egresos con montos negativos.
Incluye pruebas unitarias.
```

### 5. Pruebas

Antes de hacer commit, ejecuta las pruebas:

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Ejecutar pruebas
pytest

# Con cobertura
pytest --cov=. --cov-report=html
```

### 6. Push y Pull Request

```bash
# Push tu rama
git push origin feature/mi-nueva-funcionalidad
```

Luego crea un Pull Request en GitHub:
- Describe claramente los cambios
- Menciona issues relacionados si los hay
- Asegúrate de que el CI pase

## Estándares de Código

### Python

- Sigue PEP 8
- Usa type hints cuando sea posible
- Documenta funciones y clases con docstrings
- Máximo 100 caracteres por línea

### Estructura

- Mantén la separación MVC
- Lógica de negocio en `services/`
- Validación en `services/validators.py`
- Rutas solo para manejar requests/responses

### Pruebas

- Cobertura mínima: 80%
- Pruebas unitarias para servicios
- Pruebas de integración para rutas
- Usa fixtures de pytest

## Revisión de Código

- Todas las contribuciones requieren revisión
- Responde a comentarios de revisión
- Mantén el PR actualizado con la rama base

## Preguntas

Si tienes preguntas, abre un issue o contacta a los mantenedores.

¡Gracias por contribuir!


