# Documentación de la API REST

La API REST proporciona endpoints para todas las operaciones CRUD de la aplicación FINANZAS MALU.

## Autenticación

Todas las rutas de la API requieren autenticación mediante sesión de Flask-Login. Debes estar autenticado en la aplicación web para usar la API.

## Base URL

```
http://localhost:5000/api
```

## Formato de Respuesta

Todas las respuestas están en formato JSON. Los errores devuelven un objeto con la clave `error`:

```json
{
  "error": "Mensaje de error"
}
```

## Endpoints

### Ingresos

#### Listar Ingresos
```http
GET /api/ingresos
```

**Respuesta:**
```json
{
  "ingresos": [
    {
      "id": 1,
      "monto": 5000.00,
      "descripcion": "Salario mensual",
      "categoria": "Salario",
      "fecha": "2024-01-15"
    }
  ]
}
```

#### Crear Ingreso
```http
POST /api/ingresos
Content-Type: application/json

{
  "monto": 5000.00,
  "descripcion": "Salario mensual",
  "categoria": "Salario",
  "fecha": "2024-01-15"
}
```

**Respuesta:**
```json
{
  "message": "Ingreso creado exitosamente",
  "id": 1
}
```

#### Obtener Ingreso
```http
GET /api/ingresos/{id}
```

#### Actualizar Ingreso
```http
PUT /api/ingresos/{id}
Content-Type: application/json

{
  "monto": 5500.00,
  "descripcion": "Salario mensual actualizado",
  "categoria": "Salario",
  "fecha": "2024-01-15"
}
```

#### Eliminar Ingreso
```http
DELETE /api/ingresos/{id}
```

### Egresos

#### Listar Egresos
```http
GET /api/egresos
```

#### Crear Egreso
```http
POST /api/egresos
Content-Type: application/json

{
  "monto": 150.00,
  "descripcion": "Compra de supermercado",
  "categoria": "Alimentación",
  "fecha": "2024-01-15"
}
```

#### Obtener Egreso
```http
GET /api/egresos/{id}
```

#### Actualizar Egreso
```http
PUT /api/egresos/{id}
Content-Type: application/json

{
  "monto": 200.00,
  "descripcion": "Compra de supermercado actualizada",
  "categoria": "Alimentación",
  "fecha": "2024-01-15"
}
```

#### Eliminar Egreso
```http
DELETE /api/egresos/{id}
```

### Metas

#### Listar Metas
```http
GET /api/metas
```

**Respuesta:**
```json
{
  "metas": [
    {
      "id": 1,
      "titulo": "Vacaciones",
      "descripcion": "Ahorrar para vacaciones",
      "monto_objetivo": 10000.00,
      "monto_actual": 5000.00,
      "fecha_limite": "2024-12-31",
      "completada": false,
      "porcentaje": 50.0
    }
  ]
}
```

#### Crear Meta
```http
POST /api/metas
Content-Type: application/json

{
  "titulo": "Vacaciones",
  "descripcion": "Ahorrar para vacaciones",
  "monto_objetivo": 10000.00,
  "fecha_limite": "2024-12-31"
}
```

#### Actualizar Meta
```http
PUT /api/metas/{id}
Content-Type: application/json

{
  "titulo": "Vacaciones",
  "monto_objetivo": 12000.00,
  "monto_actual": 6000.00,
  "fecha_limite": "2024-12-31"
}
```

#### Eliminar Meta
```http
DELETE /api/metas/{id}
```

### Ahorros

#### Listar Ahorros
```http
GET /api/ahorros
```

**Respuesta:**
```json
{
  "ahorros": [
    {
      "id": 1,
      "titulo": "Ahorro mensual",
      "descripcion": "Ahorro para emergencias",
      "monto": 500.00,
      "frecuencia": "mensual",
      "fecha_inicio": "2024-01-01",
      "fecha_fin": null,
      "activo": true
    }
  ]
}
```

#### Crear Ahorro
```http
POST /api/ahorros
Content-Type: application/json

{
  "titulo": "Ahorro mensual",
  "descripcion": "Ahorro para emergencias",
  "monto": 500.00,
  "frecuencia": "mensual",
  "fecha_inicio": "2024-01-01",
  "fecha_fin": null
}
```

**Frecuencias disponibles:** `diaria`, `semanal`, `mensual`, `anual`

#### Actualizar Ahorro
```http
PUT /api/ahorros/{id}
Content-Type: application/json

{
  "titulo": "Ahorro mensual",
  "monto": 600.00,
  "frecuencia": "mensual",
  "activo": true
}
```

#### Eliminar Ahorro
```http
DELETE /api/ahorros/{id}
```

### Recordatorios

#### Listar Recordatorios
```http
GET /api/recordatorios
```

**Respuesta:**
```json
{
  "recordatorios": [
    {
      "id": 1,
      "titulo": "Pago de tarjeta",
      "descripcion": "Recordatorio de pago",
      "monto": 500.00,
      "fecha_pago": "2024-01-20",
      "fecha_recordatorio": "2024-01-18",
      "enviado": false
    }
  ]
}
```

#### Crear Recordatorio
```http
POST /api/recordatorios
Content-Type: application/json

{
  "titulo": "Pago de tarjeta",
  "descripcion": "Recordatorio de pago",
  "monto": 500.00,
  "fecha_pago": "2024-01-20",
  "fecha_recordatorio": "2024-01-18"
}
```

#### Actualizar Recordatorio
```http
PUT /api/recordatorios/{id}
Content-Type: application/json

{
  "titulo": "Pago de tarjeta actualizado",
  "monto": 550.00,
  "fecha_pago": "2024-01-20",
  "fecha_recordatorio": "2024-01-18"
}
```

#### Eliminar Recordatorio
```http
DELETE /api/recordatorios/{id}
```

### Estadísticas

#### Obtener Estadísticas
```http
GET /api/estadisticas
```

**Respuesta:**
```json
{
  "ingresos_mes": 5000.00,
  "egresos_mes": 2000.00,
  "balance_mes": 3000.00,
  "total_metas": 3,
  "metas_completadas": 1
}
```

## Códigos de Estado HTTP

- `200 OK` - Operación exitosa
- `400 Bad Request` - Error en la solicitud (datos inválidos)
- `403 Forbidden` - No autorizado (intento de acceder a recursos de otro usuario)
- `404 Not Found` - Recurso no encontrado

## Ejemplos de Uso

### Usando cURL

```bash
# Listar ingresos
curl -X GET http://localhost:5000/api/ingresos \
  -H "Cookie: session=tu-sesion-cookie"

# Crear ingreso
curl -X POST http://localhost:5000/api/ingresos \
  -H "Content-Type: application/json" \
  -H "Cookie: session=tu-sesion-cookie" \
  -d '{
    "monto": 5000.00,
    "descripcion": "Salario",
    "categoria": "Salario",
    "fecha": "2024-01-15"
  }'
```

### Usando JavaScript (fetch)

```javascript
// Listar ingresos
fetch('/api/ingresos', {
  credentials: 'include' // Incluir cookies de sesión
})
.then(response => response.json())
.then(data => console.log(data));

// Crear ingreso
fetch('/api/ingresos', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include',
  body: JSON.stringify({
    monto: 5000.00,
    descripcion: "Salario",
    categoria: "Salario",
    fecha: "2024-01-15"
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Usando Python (requests)

```python
import requests

# Iniciar sesión primero (obtener cookie de sesión)
session = requests.Session()
login_response = session.post('http://localhost:5000/login', data={
    'email': 'tu-email@example.com',
    'password': 'tu-contraseña'
})

# Listar ingresos
response = session.get('http://localhost:5000/api/ingresos')
print(response.json())

# Crear ingreso
response = session.post('http://localhost:5000/api/ingresos', json={
    'monto': 5000.00,
    'descripcion': 'Salario',
    'categoria': 'Salario',
    'fecha': '2024-01-15'
})
print(response.json())
```

## Notas Importantes

1. **Autenticación**: Todas las rutas requieren estar autenticado. La autenticación se maneja mediante cookies de sesión de Flask.

2. **Fechas**: Todas las fechas deben estar en formato ISO 8601 (YYYY-MM-DD).

3. **Montos**: Los montos deben ser números decimales válidos.

4. **Autorización**: Solo puedes acceder a tus propios recursos. Intentar acceder a recursos de otro usuario resultará en un error 403.

5. **Validación**: Todos los campos requeridos deben estar presentes en las solicitudes POST y PUT.

